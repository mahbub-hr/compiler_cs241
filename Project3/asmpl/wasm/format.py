from enum import Enum

class SectionID(Enum):
  _custom = 0
  _type = 1
  _import = 2
  _func = 3
  _table = 4
  _memory = 5
  _global = 6
  _export = 7
  _start = 8
  _element = 9
  _code = 10
  _data = 11


class SectionFormat(Enum):
  id = 0
  size = 1
  number_of_entry = 2
  cont_start = 3

class Types(Enum):
  i32 = 0x7F
  i64 = 0x7E
  f32 = 0x7D
  f64 = 0x7C
  func = 0x60

class ExportKind(Enum):
  func = 0x00
  table = 0x01
  mem = 0x02
  _global = 0x03


class Opcodes(Enum):
  block = 0x02
  loop = 0x03
  void = 0x40
  _if = 0x04
  _else =0x05  
  br = 0x0c
  br_if = 0x0d
  end = 0x0b
  call = 0x10
  ret = 0x0F
  get_local = 0x20
  set_local = 0x21
  i32_store_8 = 0x3a
  i32_const = 0x41
  i32_and = 0x71
  i32_add = 0x6A
  i32_sub = 0x6B
  i32_mul = 0x6C
  i32_div_s = 0x6D
  i32_div_u = 0x6E
  i32_trunc_f32_s = 0xA8
  i32_lt_s = 0x48
  i32_gt_s = 0x4A
  i32_le_s = 0x4C
  i32_ge_s = 0x4E
  i32_ne = 0x47
  i32_eq = 0x46


 
class MAP_SSA_TO_WASM(Enum):
  add = Opcodes.i32_add.value
  sub = Opcodes.i32_sub.value
  mul = Opcodes.i32_mul.value
  div = Opcodes.i32_div_s.value
  call = Opcodes.call.value
  ret = Opcodes.ret.value
  end = Opcodes.end.value
  blt = Opcodes.i32_lt_s.value
  bgt = Opcodes.i32_gt_s.value
  ble = Opcodes.i32_le_s.value
  bge = Opcodes.i32_ge_s.value
  bne = Opcodes.i32_ne.value
  beq = Opcodes.i32_eq.value 
  bra = Opcodes.br.value
  bra_if = Opcodes.br_if.value
  _if = Opcodes._if.value
  _else = Opcodes._else.value
  void = Opcodes.void.value
  block = Opcodes.block.value
  loop = Opcodes.loop.value

