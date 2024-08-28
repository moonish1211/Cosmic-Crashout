# Cosmic Crashout
Cosmic Crashout is a game that can be played by everyone, designed for quadriplegic individuals by utilizing the Open BCI EEG Headset. This project is made possible by PVNET Advanced Technology Center.

## Abstract
Cosmic Crashout is a Flappy Bird inspired game using Pygame and integrated EEG data inputs from the Open BCI GUI. This is one of a few games that work with the ganglion board from Open BCI.<br><br>

This project demonstrates the integration of the neurofeedback mechanism in gaming, which highlights time potential for EEG-based controls in interactive applications. 
The benefits of this game, Cosmic Crashout, is to integrate EEG data from the Open BCI GUI to allow playability for quadriplegics, using motor controls from eye movement rather than the use of the traditional hand control. Playability is still offered via keyboard controls.

Features
- Allows two inputs, blink and Hard-blink to select the options and play the game. 
- Differentiation of blind and Hard-blink to control game inputs. 
- Additionally, each of these keys are synced to the keyboard, so this game can also be played by keyboard. 
- The Local leaderboard creates a competitive environment for everyone to compete for the score in top 5. 

To get started with this project, clone the repository and install the dependencies:

https://github.com/Joe-Huber/Cosmic-Crashout.git
pip install pygame

## Game Design (Frontend)
### Controls
| Actions      | Controls | Headsets
| ----------- | ----------- |----------- |
| Select      | Enter       | Hard Blink
| Next Option | Shift        | Blink
| Jump | Space        | Blink
| Ultimate | X        | Hard Blink

### Menu
We have multiple menus in this game<br>

#### Calibration Menu: Adjusting the Hard Blink 
Calibration Menu will pop up first thing when you open the game.<br>
Make sure that the Amplitude for the FFT plot is below 10 uV and perform a hard blink when the screen shows "now"
<br><img src="Calibration.png" alt="Calibration plot" width="600"/>

#### Main Menu:
- Selecting "Start" will lead you to Game Menu to play the game
- Selecting "Quit" will exit the game
- Selecting "Settings" will navigate you to various settings in the game

#### Setting: There are few features you can adjust
- Styles: Change the spaceship
- Ability: Choose the abilities
- Difficulty: Controls the speed and the spacing of the pole

#### Game Menu: 
- Play the game by utilizing the Jump and Ultimate

#### Game Over Menu:
- Selecting "Restart" will go back to Game Menu to play the game
- Selecting "Main Menu" will go back to the Main Menu
- Selecting "Record Score" will pull you to Record Score Menu

#### Record Score Menu: Allow you to input your initial to store the score on the Local leaderboard
- Have A-Z and space as a character option
- We allow maximum of 3 character as your name
- Redirects you to the Main Menu after selecting all 3 characters

## Headset Setup Instructions
### Tools
- Open BCI GUI app
- Ganglion Board (Cyton Board will work too)
- Electrode Gel
- EEG Dongle

### Setting up Open BCI GUI
1) Launch Open BCI GUI and connect to the Ganglion Board
2) Check the Impedence as part of Setting Up Ganglion Board subsection (below)
- The game performs better with lower impedance values, you should strive for values below 50 in channels 1 and 3, but high values can be tolerated as we mostly worked on values above 150
3) Adjust the setting on FFT Plot
    - Filter only channel 1 and 3
    - Adjust the scale of the plot<br>
    - TIP: Make sure that these two plot is sitting under Amplitude of 8
<br><img src="Readme_image/FFT_plot.png" alt="FFT PLOT" width="600"/>
4) Open Networking tab and copy the setting to click "start UDP Stream"<br>
<br><img src="Readme_image/UDP_Image.png" alt="FFT PLOT" width="600"/>
5) Click "Start Data Steam" on the top left corner
6) Start playing the game!



### Setting up the Ganglion Board
We need total of 2 channels connected to Ganglion Board
<br>Tip: Chose the location where the impedence check is the lowest, adding Gel will improve impedence significantly.
- Channel 1: FP1 or FP2
- Channel 3: O1 or O2

Set up Noise Canceling and Reference by having clip on the ear<br>
Please Reference [Open BCI Documentation](https://docs.openbci.com/) for specific setups

Here is the Impedence we are working on. We are interested in channel 1(261.0) and 3 (159.0)<br>
![Alt text](Readme_image/Impedence.png "Impedence Result")


## EEG Analysis (Backend)
EEG Analysis team first researched different controls that may be extracted for the game, but soon realized the limits from using Ganglion board which has fewer channels than the Cyton board. Because of EEG headset's nature of being influenced from the external factor such as electromagnetic waves, our team were having trouble recording data consistly. 
<br>After weeks of researching the best controls that can be used, we concluded that blinking is by far consistent and stable. 
<br><img src="Readme_image/blink.png" alt="Blink shown on FFT plot" width="600"/>
<br>As you can see, whenever the subject blinks, FFT plot represent these as a concave indicating the high amplitude. From this mechanism, we decided to detect a blink whenever the amplitue first goes above 8 and when the average amplitude first starts increasing. 
<br><img src="Readme_image/hard_blink.png" alt="Hard Blink shown on FFT plot" width="600"/>
<br>Similarily, a hard blink is detected whenever the amplitude exceeds the specified threshold that was calculated from the calibration menu.
<br>The calibration menu forces the user to blink when the screen prints "now". Using this data, we can calculate the maximum average amplitude from hard blinks in both channels. 
This means that the threshold is unique for each user, which allows flexibility for who can play the game.
In order for the data to be extracted in real time, our team utilized UDP to recieve FFT data from Open BCI's GUI. 
We filter the frequencies to range from 4.8 to 17.6 and processed the corresponding amplitude. 
Once we detected the two controls, we synced them to the game to be played by the users.

## Background 
This project was made possible by PVNets amazing internship program. This goal with this project was to expand the accessibility to esports and gaming in general to quadriplegics and other disabled peoples. We were inspired by various cyborg olympics such as the cybathalon and the robohub cyborg olympics. Through our work, we hoped to share our research and developments to hopefully stand as a stepping stone for future research in this field and to act as an example for what is possible with EEG data.

## Aspects of improvement
One aspects of improvement is the number of controls and how we input controls. Earlier in our research, we looked into SSVEP and P300 types of input, which would give information to the game using flashing images and lights. Another type of input we researched was motor control, which we deemed too difficult when limited to 4 channels, but if we found a method for it to work, we would be able to input controls based solely on the user imagining using limbs. <br>
Another area in which we could improve is the game design aspect. The intention behind our design was to demonstrate an example for how our method of blinking incorporated into the game, and so improvements could be made on the game design aspect. Some changes could be progressive difficulty change, more abilities and difficulties, or simply designing a new game as the current one is intended to be viewed as a prototype.

## Team Member
Ted Vegvari: Director of Research Development <br>
Jill Luna Nomura: EEG Data Analysis Lead, Open BCI Integration Development Lead, Leaderboard Management Integration <br>
Patrick McGrath: UI & Game strategy Development Lead, BCI Interface Integration & Accessibility Development, Open BCI Integration Development<br>
Joe Hubor: BCI Interface Integration & Accessibility Development Lead, UI & Game strategy Development, Quality Assurance Testor 2<br>
Tommy Nguyen: EEG Headset Electronic Integration, Visual & Asset Development, Quality Assurance Testor <br>
Joshua Nwabuzor: Visual & Asset Development, BCI Interface Integration & Accessibility Development<br>
Mark Segal: UI & Game strategy Development<br>
Mathias Gutierrez: Sound Design<br>
Daniel Belonio: UI & Game strategy Development<br>



