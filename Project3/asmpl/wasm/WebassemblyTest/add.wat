(module
  (import "console" "log" (func (param i64)))
  (func (export "main")
    i64.const 1
    i64.const 2
    i64.add
    call 0))