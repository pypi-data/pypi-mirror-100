# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# ********************************************* LLVM bindings **************************************************************

import atexit
import ctypes
import enum
import functools
import inspect
from llvmlite import ir
import numpy as np
import os
import re
from typing import Set
import weakref
from psyneulink.core.scheduling.time import Time
from psyneulink.core.globals.sampleiterator import SampleIterator
from psyneulink.core.globals.utilities import ContentAddressableList
from psyneulink.core import llvm as pnlvm
from . import codegen
from .debug import debug_env

__all__ = ['LLVMBuilderContext', '_modules', '_find_llvm_function']


_modules: Set[ir.Module] = set()
_all_modules: Set[ir.Module] = set()
_struct_count = 0


@atexit.register
def module_count():
    if "stat" in debug_env:
        print("Total LLVM modules: ", len(_all_modules))
        print("Total structures generated: ", _struct_count)
        s = LLVMBuilderContext.get_global()
        print("Total generations by global context: {}".format(s._llvm_generation))
        print("Object cache in global context: {} hits, {} misses".format(s._stats["cache_requests"] - s._stats["cache_misses"], s._stats["cache_misses"]))
        for stat in ("input", "output", "param", "state", "data"):
            gen_stat = s._stats[stat + "_structs_generated"]
            print("Total {} structs generated by global context: {}".format(stat, gen_stat))
        print("Total python types converted by global context: {}".format(s._stats["types_converted"]))




_BUILTIN_PREFIX = "__pnl_builtin_"
_builtin_intrinsics = frozenset(('pow', 'log', 'exp', 'tanh', 'coth', 'csch', 'is_close'))


class _node_wrapper():
    def __init__(self, composition, node):
        self._comp = composition
        self._node = node

    def _gen_llvm_function(self, *, ctx, tags:frozenset):
        return codegen.gen_node_wrapper(ctx, self._comp, self._node, tags=tags)

def _comp_cached(func):
    @functools.wraps(func)
    def wrapper(bctx, obj):
        try:
            obj_cache = bctx._cache.setdefault(obj, dict())
        except TypeError:  # 'super()' references can't be cached
            obj_cache = None
        else:
            if func in obj_cache:
                return obj_cache[func]
        val = func(bctx, obj)
        if obj_cache is not None:
            obj_cache[func] = val
        return val

    return wrapper


class LLVMBuilderContext:
    __global_context = None
    __uniq_counter = 0
    _llvm_generation = 0
    int32_ty = ir.IntType(32)
    float_ty = ir.DoubleType()
    bool_ty = ir.IntType(1)

    def __init__(self):
        self._modules = []
        self._cache = weakref.WeakKeyDictionary()
        self._stats = { "cache_misses":0,
                        "cache_requests":0,
                        "types_converted":0,
                        "param_structs_generated":0,
                        "state_structs_generated":0,
                        "data_structs_generated":0,
                        "input_structs_generated":0,
                        "output_structs_generated":0,
                      }

    def __enter__(self):
        module = ir.Module(name="PsyNeuLinkModule-" + str(LLVMBuilderContext._llvm_generation))
        self._modules.append(module)
        LLVMBuilderContext._llvm_generation += 1
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        assert len(self._modules) > 0
        module = self._modules.pop()
        _modules.add(module)
        _all_modules.add(module)

    @property
    def module(self):
        assert len(self._modules) > 0
        return self._modules[-1]

    @classmethod
    def get_global(cls):
        if cls.__global_context is None:
            cls.__global_context = LLVMBuilderContext()
        return cls.__global_context

    @classmethod
    def get_unique_name(cls, name: str):
        cls.__uniq_counter += 1
        name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        return name + '_' + str(cls.__uniq_counter)

    def get_builtin(self, name: str, args=[], function_type=None):
        if name in _builtin_intrinsics:
            return self.import_llvm_function(_BUILTIN_PREFIX + name)
        if name in ('maxnum'):
            function_type = pnlvm.ir.FunctionType(args[0], [args[0], args[0]])
        return self.module.declare_intrinsic("llvm." + name, args, function_type)

    def create_llvm_function(self, args, component, name=None, *, return_type=ir.VoidType(), tags:frozenset=frozenset()):
        name = "_".join((str(component), *tags)) if name is None else name

        # Builtins are already unique and need to keep their special name
        func_name = name if name.startswith(_BUILTIN_PREFIX) else self.get_unique_name(name)
        func_ty = pnlvm.ir.FunctionType(return_type, args)
        llvm_func = pnlvm.ir.Function(self.module, func_ty, name=func_name)
        llvm_func.attributes.add('argmemonly')
        for a in llvm_func.args:
            if isinstance(a.type, ir.PointerType):
                a.attributes.add('nonnull')

        metadata = self.get_debug_location(llvm_func, component)
        if metadata is not None:
            scope = dict(metadata.operands)["scope"]
            llvm_func.set_metadata("dbg", scope)

        # Create entry block
        block = llvm_func.append_basic_block(name="entry")
        builder = pnlvm.ir.IRBuilder(block)
        builder.debug_metadata = metadata

        return builder

    def gen_llvm_function(self, obj, *, tags:frozenset) -> ir.Function:
        obj_cache = self._cache.setdefault(obj, dict())

        self._stats["cache_requests"] += 1
        if tags not in obj_cache:
            self._stats["cache_misses"] += 1
            with self:
                obj_cache[tags] = obj._gen_llvm_function(ctx=self, tags=tags)
        return obj_cache[tags]

    def import_llvm_function(self, fun, *, tags:frozenset=frozenset()) -> ir.Function:
        """
        Get function handle if function exists in current modele.
        Create function declaration if it exists in a older module.
        """
        if isinstance(fun, str):
            f = _find_llvm_function(fun, _all_modules | {self.module})
        else:
            f = self.gen_llvm_function(fun, tags=tags)

        # Add declaration to the current module
        if f.name not in self.module.globals:
            decl_f = ir.Function(self.module, f.type.pointee, f.name)
            assert decl_f.is_declaration
            return decl_f
        return f

    @staticmethod
    def get_debug_location(func: ir.Function, component):
        if "debug_info" not in debug_env:
            return

        mod = func.module
        path = inspect.getfile(component.__class__) if component is not None else "<pnl_builtin>"
        d_version = mod.add_metadata([ir.IntType(32)(2), "Dwarf Version", ir.IntType(32)(4)])
        di_version = mod.add_metadata([ir.IntType(32)(2), "Debug Info Version", ir.IntType(32)(3)])
        flags = mod.add_named_metadata("llvm.module.flags")
        if len(flags.operands) == 0:
            flags.add(d_version)
            flags.add(di_version)
        cu = mod.add_named_metadata("llvm.dbg.cu")
        di_file = mod.add_debug_info("DIFile", {
            "filename": os.path.basename(path),
            "directory": os.path.dirname(path),
        })
        di_func_type = mod.add_debug_info("DISubroutineType", {
            # None as `null`
            "types": mod.add_metadata([None]),
        })
        di_compileunit = mod.add_debug_info("DICompileUnit", {
            "language": ir.DIToken("DW_LANG_Python"),
            "file": di_file,
            "producer": "PsyNeuLink",
            "runtimeVersion": 0,
            "isOptimized": False,
        }, is_distinct=True)
        cu.add(di_compileunit)
        di_func = mod.add_debug_info("DISubprogram", {
            "name": func.name,
            "file": di_file,
            "line": 0,
            "type": di_func_type,
            "isLocal": False,
            "unit": di_compileunit,
        }, is_distinct=True)
        di_loc = mod.add_debug_info("DILocation", {
            "line": 0, "column": 0, "scope": di_func,
        })
        return di_loc

    @_comp_cached
    def get_input_struct_type(self, component):
        self._stats["input_structs_generated"] += 1
        if hasattr(component, '_get_input_struct_type'):
            return component._get_input_struct_type(self)

        default_var = component.defaults.variable
        return self.convert_python_struct_to_llvm_ir(default_var)

    @_comp_cached
    def get_output_struct_type(self, component):
        self._stats["output_structs_generated"] += 1
        if hasattr(component, '_get_output_struct_type'):
            return component._get_output_struct_type(self)

        default_val = component.defaults.value
        return self.convert_python_struct_to_llvm_ir(default_val)

    @_comp_cached
    def get_param_struct_type(self, component):
        self._stats["param_structs_generated"] += 1
        if hasattr(component, '_get_param_struct_type'):
            return component._get_param_struct_type(self)

        def _param_struct(p):
            val = p.get(None)   # this should use defaults
            if hasattr(val, "_get_compilation_params") or \
               hasattr(val, "_get_param_struct_type"):
                return self.get_param_struct_type(val)
            if isinstance(val, ContentAddressableList):
                return ir.LiteralStructType(self.get_param_struct_type(x) for x in val)
            elif p.name == 'matrix':   # Flatten matrix
                val = np.asfarray(val).flatten()
            elif p.name == 'num_estimates':  # Should always be int
                val = np.int32(0) if val is None else np.int32(val)
            elif np.ndim(val) == 0 and component._is_param_modulated(p):
                val = [val]   # modulation adds array wrap
            return self.convert_python_struct_to_llvm_ir(val)

        elements = map(_param_struct, component._get_compilation_params())
        return ir.LiteralStructType(elements)

    @_comp_cached
    def get_state_struct_type(self, component):
        self._stats["state_structs_generated"] += 1
        if hasattr(component, '_get_state_struct_type'):
            return component._get_state_struct_type(self)

        def _state_struct(p):
            val = p.get(None)   # this should use defaults
            if hasattr(val, "_get_compilation_state") or \
               hasattr(val, "_get_state_struct_type"):
                return self.get_state_struct_type(val)
            if isinstance(val, ContentAddressableList):
                return ir.LiteralStructType(self.get_state_struct_type(x) for x in val)
            struct = self.convert_python_struct_to_llvm_ir(val)
            return ir.ArrayType(struct, p.history_min_length + 1)

        elements = map(_state_struct, component._get_compilation_state())
        return ir.LiteralStructType(elements)

    @_comp_cached
    def get_data_struct_type(self, component):
        self._stats["data_structs_generated"] += 1
        if hasattr(component, '_get_data_struct_type'):
            return component._get_data_struct_type(self)

        return ir.LiteralStructType([])

    def get_node_wrapper(self, composition, node):
        cache = getattr(composition, '_node_wrappers', None)
        if cache is None:
            cache = dict()
            setattr(composition, '_node_wrappers', cache)
        return cache.setdefault(node, _node_wrapper(composition, node))

    def convert_python_struct_to_llvm_ir(self, t):
        self._stats["types_converted"] += 1
        if t is None:
            return ir.LiteralStructType([])
        elif type(t) is list:
            if len(t) == 0:
                return ir.LiteralStructType([])
            elems_t = [self.convert_python_struct_to_llvm_ir(x) for x in t]
            if all(x == elems_t[0] for x in elems_t):
                return ir.ArrayType(elems_t[0], len(elems_t))
            return ir.LiteralStructType(elems_t)
        elif type(t) is tuple:
            elems_t = [self.convert_python_struct_to_llvm_ir(x) for x in t]
            if len(elems_t) > 0 and all(x == elems_t[0] for x in elems_t):
                return ir.ArrayType(elems_t[0], len(elems_t))
            return ir.LiteralStructType(elems_t)
        elif isinstance(t, enum.Enum):
            # FIXME: Consider enums of non-int type
            assert all(round(x.value) == x.value for x in type(t))
            return self.int32_ty
        elif isinstance(t, (int, float, np.floating)):
            return self.float_ty
        elif isinstance(t, np.integer):
            # Python 'int' is handled above as it is the default type for '0'
            return ir.IntType(t.nbytes * 8)
        elif isinstance(t, np.ndarray):
            return self.convert_python_struct_to_llvm_ir(t.tolist())
        elif isinstance(t, np.random.RandomState):
            return pnlvm.builtins.get_mersenne_twister_state_struct(self)
        elif isinstance(t, Time):
            return ir.ArrayType(self.int32_ty, len(Time._time_scale_attr_map))
        elif isinstance(t, SampleIterator):
            if isinstance(t.generator, list):
                return ir.ArrayType(self.float_ty, len(t.generator))
            # Generic iterator is {start, increment, count}
            return ir.LiteralStructType((self.float_ty, self.float_ty, self.int32_ty))
        assert False, "Don't know how to convert {}".format(type(t))


def _find_llvm_function(name: str, mods=_all_modules) -> ir.Function:
    f = None
    for m in mods:
        if name in m.globals:
            f = m.get_global(name)

    if not isinstance(f, ir.Function):
        raise ValueError("No such function: {}".format(name))
    return f


def _gen_cuda_kernel_wrapper_module(function):
    module = ir.Module(name="wrapper_" + function.name)

    decl_f = ir.Function(module, function.type.pointee, function.name)
    assert decl_f.is_declaration
    orig_args = function.type.pointee.args

    # remove indices if this is grid_evauate_ranged
    is_grid_ranged = len(orig_args) == 7 and isinstance(orig_args[2], ir.IntType)
    if is_grid_ranged:
        orig_args = orig_args[:2] + orig_args[4:]

    wrapper_type = ir.FunctionType(ir.VoidType(), [*orig_args, ir.IntType(32)])
    kernel_func = ir.Function(module, wrapper_type, function.name + "_cuda_kernel")
    # Add kernel mark metadata
    module.add_named_metadata("nvvm.annotations", [kernel_func, "kernel", ir.IntType(32)(1)])

    # Start the function
    block = kernel_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # Calculate global id of a thread in x dimension
    intrin_ty = ir.FunctionType(ir.IntType(32), [])
    tid_x_f = ir.Function(module, intrin_ty, "llvm.nvvm.read.ptx.sreg.tid.x")
    ntid_x_f = ir.Function(module, intrin_ty, "llvm.nvvm.read.ptx.sreg.ntid.x")
    ctaid_x_f = ir.Function(module, intrin_ty, "llvm.nvvm.read.ptx.sreg.ctaid.x")
    global_id = builder.mul(builder.call(ctaid_x_f, []), builder.call(ntid_x_f, []))
    global_id = builder.add(global_id, builder.call(tid_x_f, []))

    # Check global id and exit if we're over
    should_quit = builder.icmp_unsigned(">=", global_id, kernel_func.args[-1])
    with builder.if_then(should_quit):
        builder.ret_void()

    # Index all pointer arguments. Ignore the thread count argument
    args = list(kernel_func.args)[:-1]
    indexed_args = []

    # If we're calling ranged search there are no offsets
    if is_grid_ranged:
        next_id = builder.add(global_id, global_id.type(1))
        call_args = args[:2] + [global_id, next_id] + args[2:]
        builder.call(decl_f, call_args)
        builder.ret_void()
        return module


    # There are 6 arguments to evaluate:
    # comp_param, comp_state, allocations, output, input, comp_data
    is_grid_evaluate = len(args) == 6

    # Runs need special handling. data_in and data_out are one dimensional,
    # but hold entries for all parallel invocations.
    # comp_state, comp_params, comp_data, comp_in, comp_out, #trials, #inputs
    is_comp_run = len(args) == 7
    if is_comp_run:
        runs_count = builder.load(args[5])
        input_count = builder.load(args[6])

    for i, arg in enumerate(args):
        if isinstance(arg.type, ir.PointerType):
            offset = global_id
            if is_comp_run:
                # #inputs needs to be the same for comp run
                if i == 6:
                    offset = ir.IntType(32)(0)
                # data arrays need special handling
                elif i == 4:  # data_out
                    offset = builder.mul(global_id, runs_count)
                elif i == 3:  # data_in
                    offset = builder.mul(global_id, input_count)
            elif is_grid_evaluate:
                # all but #2 and #3 are shared
                if i != 2 and i != 3:
                    offset = ir.IntType(32)(0)

            arg = builder.gep(arg, [offset])

        indexed_args.append(arg)
    builder.call(decl_f, indexed_args)
    builder.ret_void()

    return module


@functools.lru_cache(maxsize=128)
def _convert_llvm_ir_to_ctype(t: ir.Type):
    type_t = type(t)

    if type_t is ir.VoidType:
        return None
    elif type_t is ir.IntType:
        if t.width == 8:
            return ctypes.c_int8
        elif t.width == 16:
            return ctypes.c_int16
        elif t.width == 32:
            return ctypes.c_int32
        elif t.width == 64:
            return ctypes.c_int64
        else:
            assert False, "Unknown integer type: {}".format(type_t)
    elif type_t is ir.DoubleType:
        return ctypes.c_double
    elif type_t is ir.FloatType:
        return ctypes.c_float
    elif type_t is ir.PointerType:
        pointee = _convert_llvm_ir_to_ctype(t.pointee)
        ret_t = ctypes.POINTER(pointee)
    elif type_t is ir.ArrayType:
        element_type = _convert_llvm_ir_to_ctype(t.element)
        ret_t = element_type * len(t)
    elif type_t is ir.LiteralStructType:
        global _struct_count
        uniq_name = "struct_" + str(_struct_count)
        _struct_count += 1

        field_list = []
        for i, e in enumerate(t.elements):
            # llvmlite modules get _unique string only works for symbol names
            field_uniq_name = uniq_name + "field_" + str(i)
            field_list.append((field_uniq_name, _convert_llvm_ir_to_ctype(e)))

        ret_t = type(uniq_name, (ctypes.Structure,), {"__init__": ctypes.Structure.__init__})
        ret_t._fields_ = field_list
        assert len(ret_t._fields_) == len(t.elements)
    else:
        assert False, "Don't know how to convert LLVM type: {}".format(t)

    return ret_t
