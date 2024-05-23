(module
  ;; Import external functions for input and output.
  (import "console" "log" (func $OutputNum (param i32)))

  ;; Define memory
  (memory 1)

  ;; Define a main function
  (func $main
    ;; Initialize local variables a, b, c, d, e
  	(local i32)
    i32.const 2
    local.set 0 ;; Store result in local variable a
    
      
    local.get 0 ;; Get a
    local.get 0

    i32.add 
    i32.const 0

    i32.lt_s ;; Check if a < 0
    if
        local.get 0
        i32.const 1
        i32.add
        local.set 0 ;; Set a = a + 1
    else
        local.get 0
        i32.const 1
        i32.sub
        local.set 0 ;; Set a = a - 1
    end
    
    local.get 0 ;; Get b
    local.get 0
    i32.add
    local.set 0 ;; Set d = b + 1 (d is local var 3)
    
    ;; Output a, b, and c
    local.get 0
    call $OutputNum
  )

  
  
  ;; Start the main function on load
  (start $main)
)