(module
	(import "console" "log" (func (param i32)))
    (func (export "main")
		i32.const 43
		i32.const 54
		i32.add
		call 0)
)