make
srec_cat @srec/concat.txt
srec_cat @srec/Hex_Signed.txt
srec_cat @srec/unfill.txt
srec_cat @srec/convert.txt
openocd -f interface/stlink.cfg -f board/stm32f103c8_blue_pill.cfg -c "program App.bin 0x08000000 reset exit"