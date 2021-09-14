make
srec_cat @srec/concat.txt
srec_cat @srec/Hex_Signed.txt
srec_cat @srec/unfill.txt
openocd -f interface/stlink.cfg -f board/stm32f103c8_blue_pill.cfg -c "program App.hex  reset exit"