(module
(import "console" "log" (func (param i64)))
   (func (local i64)(local i64)
        (local.set 0 (i64.const 3))
        (local.set 1 (i64.const 12))
        local.get 0
        local.get 1
        i64.add
        call 0
        )

        (start 1)

)
