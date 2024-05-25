(module
  (import "console" "log" (func (param i32)))
  (func (export "main")
    i32.const 1
    i32.const 2
    i32.add
    call 0))