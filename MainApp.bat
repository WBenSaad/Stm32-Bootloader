cd MainApp
make
cd ..
srec_cat @srec/ChecksumAdd.txt
openocd -f interface/stlink.cfg -f board/stm32f103c8_blue_pill.cfg -c "program App.bin 0x08004000 reset exit"