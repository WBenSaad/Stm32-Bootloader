

# STM32 Bootloader 

## Table of contents

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>  
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#hardware-requirements">Hardware Requirements</a></li>
        <li><a href="#software-requirements">Software Requirements</a></li>
      </ul>
    </li>
      <ul>
    </ul>
 </li> 
    <li><a href="#software-implementation">Software implementation</a></li>
    <li><a href="#executing-the-program">Executing the program</a></li>
    <li><a href="#conclusion-and-perspective">Conclusion and perspective</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
    
    
  </ol>
</details>

   
## About the project

![image](https://user-images.githubusercontent.com/86969450/128428449-4470b309-326e-4470-a66a-8fdc706914c3.png)


Project is an STM32 Bootloader capable of performing in-application-programming through UART ,as well Image validity verification on each start-up with a Checksum

## Capabilities
* Flash Programming through  USART 
* Flash verification after programming
* Checksum verification

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
* ARM GCC  :  For Compilation and generation of an Image
* OpenOCD  :  For flashing to the target
* SRecord  :  Will append a Checksum at the end of the Image


### Microcontroller set up  
Using CubeMX , we set the USART1 peripheral : PA10 as  RX and PA9 as TX.
We need another pin as Input to read the push Button value . I used PIN PB12.
![image](https://user-images.githubusercontent.com/33790012/136715859-4d3c0550-9772-4e1e-b0cb-ad01ea956e2e.png)

    
### How to use
1- Flash the Bootloader using


### Memory Map
We modify the memory layout the generated programs through the Linker Scripts and it goes as follows :
![image](https://user-images.githubusercontent.com/33790012/136716066-9241d08c-e75c-4617-a23b-aa81d45b4f8b.png)
We Will allocate 16K for the Bootloader and the Rest of the flash will be split between our main app and an eventual Backup.
Moreover we may need a shared memory that will allow the communication between the Bootloader and the App.
It will be defined as noinit so that it survives soft resets and doesn't get initialized on every start-up.
![image](https://user-images.githubusercontent.com/33790012/136716184-c22fb8a4-8797-4302-a194-4e4525436a20.png)

### Appending an Image Checksum at the end of the Binary using Srecord
 
 After generating our App binary we will use SRecord to append at the end of it a checksum.
 SRecord can generate a valid stm32 CRC checksum and put at any place in the binary.
 It will be stored at the end of the binary file.
 
###
 



