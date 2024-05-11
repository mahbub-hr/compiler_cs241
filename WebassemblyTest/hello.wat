(module
	(import "console" "log" (func $log(param i32)))
    (func (export "main")
		i32.const 43
		call $log)
)