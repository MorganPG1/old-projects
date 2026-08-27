

ld a, $68
ld cd, $8001
call Setdata

inc a
ld cd, $8002
call Setdata
ld a, $FF
ld cd, $FFFF
call Setdata
jp (0000)

:Setdata
ld (cd), a
ret