(module
(import "console" "log" (func (param i32)))
   (func (local i32)(local i32)
        (local.set 0 (i32.const 3))
        (local.set 1 (i32.const 12))
        local.get 0
        local.get 1
        i32.add
        call 0
        )

        (start 1)

)
