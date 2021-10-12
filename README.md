

# STM32 Bootloader 

## Table of contents

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>  
    <li><a href="#Capabilities">Capabilities</a>
    <li><a href="#Prerequisites">Prerequisites</a></li>
    <li><a href="#Microcontroller-Configuration">Microcontroller Configuration</a></li>
    <li><a href="#Memory-Map">Memory Map</a></li>
    <li><a href="#Generating-a-Checksum-using-Srecord">Generating a Checksum  using Srecord</a></li>
    <li><a href="#Behaviour-Overview">Bootloader implementation</a></li>
      <ul>
        <li><a href="#General-system-Behaviour">Bootloader implementation</a></li>
        <li><a href="#Bootloader-Behaviour">Bootloader implementation</a></li>
      </ul>
    <li><a href="#Code">Code</a></li>
    <li><a href="#Host-App">HOST APP</a></li>
    <li><a href="#Usage">Usage</a></li>
    <li><a href="#Refrences">Refrences</a></li>
    
    
    
  </ol>
</details>

   
## About the project


Project is an STM32 Bootloader capable of performing in-application-programming through UART ,as well Image validity verification on each start-up. 

## Capabilities
* Flash Programming through  USART 
* Image Integrity Verification
* Robust data transfer

<!-- GETTING STARTED -->

### Prerequisites
* ARM GCC  :  For compilation.
* OpenOCD  :  Will be used to Flash the Bootloader.
* SRecord  :  Will be generate the App Checksum Post Build.
* Python 3 :  For the App that will send the Binary File to the MCU.


### Microcontroller Configuration  
Using CubeMX , we set the USART1 peripheral : PA10 as  RX and PA9 as TX.
We need another pin as Input to read the push Button value . I used PIN PB12.
A press to the push-Button will force the MCU into flashing Mode.
![image](https://user-images.githubusercontent.com/33790012/136715859-4d3c0550-9772-4e1e-b0cb-ad01ea956e2e.png)


### Memory Map
We modify the memory layout the generated programs through the Linker Scripts and it goes as follows :
![image](https://user-images.githubusercontent.com/33790012/136716066-9241d08c-e75c-4617-a23b-aa81d45b4f8b.png)
We Will allocate 16K for the Bootloader and the Rest of the flash will be split between our main app and an eventual Backup.
Moreover we may need a shared memory that will allow the communication between the Bootloader and the App.
It will be defined as noinit so that it survives soft resets and doesn't get initialized on every start-up.
If the User presses the Push-Button when in App is running ,the system will do a soft reset and Boot variable will be set which will allow the UC to go into flashing mode.
![image](https://user-images.githubusercontent.com/33790012/136716184-c22fb8a4-8797-4302-a194-4e4525436a20.png)

### Generating a Checksum  using Srecord
 
 After generating our App binary we will use SRecord to append at the end of it a checksum.  
 SRecord can generate a valid stm32 CRC checksum and put at any place in the binary.  
 It will be stored at the end of the binary file.  
 SRecord Script is under /srec and is thoroughly commented.
 
### Behaviour overview 
#### General system Behaviour
Entire system Behaviour 
![image](https://user-images.githubusercontent.com/33790012/136871514-b3e10559-295c-42e1-8e31-af3137a2bc82.png)

#### Bootloader Behaviour 
The bootloader will enter flashing mode in 4 differents cases : 
1. There is no App in memory Basically the start Address of the App section will have 0xFFFF
2. An invalid App Image bascially The Checksum Calculated at the start of the Bootloader doesn't match the one generated beforehand with Srecord
3. Button was pressed during start-up
4. An application request , which means the Button was pressed when App was running and it was forced to reset and go into Flash Mode


The General behaviour of the Bootloader is described in this graph :
![image](https://user-images.githubusercontent.com/33790012/136867880-3dff74dd-f520-4f82-af46-32d47cb58973.png)

The packet received are 132 bytes long and are formed like this :
![image](https://user-images.githubusercontent.com/33790012/136940473-2e28eb81-c152-48a8-a7b5-602fb61e777b.png)  
If CRC doesn't match then the Bootloader will request a resend from the Host Application


#### Code
The Bootloader is implemented under /Bootloader/SRC and the Main App is under /MainApp/src.  
Everything else is provided by ST.

### Host App

App is executed from Terminal and the USART configuration is done through the Command Line as well.  
For example to have a USART configured as 115200 baud rate and COM10 you would write :
```
python3 Flasher.py -n "AppBinaryName" -b 115200 -p COM10
```
Different parameters can be configured through the command Line just type in 
```
python3 Flasher.py -h
```
to visualize all of them.  
3 Flags are obligatory : The Filename,the Port and the Baud Rate.


### Usage
1- Compile then Flash the Bootloader into your MCU with the script: 
```
bash Bootloader.sh 
```
2- Compilation of the App and Signing it with SRecord can be done with :
```
bash MainApp.sh 
```
3- Send your Binary file to UC with the following :
```
python3 Flasher.py -n "APP_NAME" -b BAUD RATE -p "Port"
```
The name of the Image,the baud rate and the Port are the only compulsory parameters. For more details on all 
the flags please look at Section "Host App".


### Refrences 

[STM32 Reference Manual](https://www.st.com/resource/en/reference_manual/cd00171190-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-arm-based-32-bit-mcus-stmicroelectronics.pdf)  
[AN4187 : CRC on STM32](https://www.st.com/resource/en/application_note/an4187-using-the-crc-peripheral-in-the-stm32-family-stmicroelectronics.pdf)  

Bootloader Design Refrences :    
[Memfault's Bootloader from scratch](https://interrupt.memfault.com/blog/how-to-write-a-bootloader-from-scratch)     
[Memfault's Device Firmware cookbook](https://interrupt.memfault.com/blog/device-firmware-update-cookbook)  
[Beningo's Blog](https://www.beningo.com/wp-content/uploads/images/Papers/bootloader_design_for_microcontrollers_in_embedded_systems%20.pdf)   

SRecord Refrences :  
[The official Manual](http://srecord.sourceforge.net/srecord-1.64.pdf)    
[EEV Blog](https://www.eevblog.com/forum/microcontrollers/stm32-hex-file-signing-with-crc/)    
[SourceForge thread](https://sourceforge.net/p/srecord/discussion/248569/thread/b8fac9db76/?limit=25)    




 



