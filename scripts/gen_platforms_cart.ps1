# ----------------------
# Acorn Electron
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key acorn-electron `
    --platform-name-full "Acorn Electron" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput electron -cart1" `
    --output-format yaml `
    --output-file system_softlist.yml `
    electron

# ----------------------
# Amstrad GX4000
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key amstrad-gx4000 `
    --platform-name-full "Amstrad GX4000" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gx4000 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    gx4000

# ----------------------
# Atari XEGS
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key atari-xegs `
    --platform-name-full "Atari XEGS" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput xegs -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    xegs

# ----------------------
# Bally Astrocade
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key bally-astrocade `
    --platform-name-full "Bally Astrocade" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput astrocde -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    astrocde

# ----------------------
# Bambino Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key bambino-handhelds-lcd `
    --platform-name-full "Bambino Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems bambball bmboxing bmcfball bmsafari bmsoccer splasfgt ssfball ufombs

# ----------------------
# Bandai Gundam RX-78
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key bandai-gundam-rx-78 `
    --platform-name-full "Bandai Gundam RX-78" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput rx78 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    rx78

# ----------------------
# Bandai Handheld (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key bandai-handhelds-lcd `
    --platform-name-full "Bandai Handheld (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems bbtime bcclimbr bcheetah bdoramon bfriskyt bgalaxn bgunf bpengo bultrman bzaxxon ggdman ktparman machiman paccon packmon pairmtch racetime tc7atc tkjmaru uboat zackman

# ----------------------
# Bandai Let's! TV Play
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key bandai-lets-tv-play `
    --platform-name-full "Bandai Let's! TV Play" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --fuzzy ban_ `
    --include-systems anpantv dmbtjunc dmnslayg paccon ltv_naru ltv_tam maxheart mrangbat namcons1 namcons2 taitons1 taitons2

# ----------------------
# Bandai Super Note Club
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key bandai-super-note-club `
    --platform-name-full "Bandai Super Note Club" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput snotec -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    snotec

# ----------------------
# Bandai Super Vision 8000
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key bandai-super-vision-8000 `
    --platform-name-full "Bandai Super Vision 8000" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput sv8000 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    sv8000

# ----------------------
# Bandai Tamagotchi
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key bandai-tamagotchi `
    --platform-name-full "Bandai Tamagotchi" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems digimon digimonv2 digimonv3 tama tamaang tamag2 tamamot tamapix tamamot

# ----------------------
# Bit Corp Gamate
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key bit-corp-gamate `
    --platform-name-full "Bit Corp Gamate" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gamate -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    gamate

# ----------------------
# Casio Loopy
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key casio-loopy `
    --platform-name-full "Casio Loopy" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput casloopy -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    casloopy

# ----------------------
# Casio PV-1000
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key casio-pv-1000 `
    --platform-name-full "Casio PV-1000" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput pv1000 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    pv1000

# ----------------------
# Casio PV-2000
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key casio-pv-2000 `
    --platform-name-full "Casio PV-2000" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput pv2000 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    pv2000

# ----------------------
# Coleco Handheld (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key coleco-handhelds-lcd `
    --platform-name-full "Coleco Handheld (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems alnattck amaztron cdkong cgalaxn cmspacmn cpacman cpacmanr1 cqback cfrogger

# ----------------------
# Commodore VIC-10
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key commodore-vic-10 `
    --platform-name-full "Commodore VIC-10" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vic10 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    vic10

# ----------------------
# Commodore VIC-20
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key commodore-vic-20 `
    --platform-name-full "Commodore VIC-20" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vic1001 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    vic1001

# ----------------------
# Conny TV Games
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key conny-tv-games `
    --platform-name-full "Conny TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems conyteni pdc100 conyfght conyping dorapdc pdc150t pdc200 pdc40t pdc50 tmntpdc vjpp2

# ----------------------
# Creatronic Mega Duck
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key creatronic-mega-duck `
    --platform-name-full "Creatronic Mega Duck" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput megaduck -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    megaduck

# ----------------------
# Dragon
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key dragon `
    --platform-name-full "Dragon" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput dragon64 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    dragon64

# ----------------------
# Emerson Arcadia 2001
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key emerson-arcadia-2001 `
    --platform-name-full "Emerson Arcadia 2001" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput arcadia -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    arcadia

# ----------------------
# Entex Adventure Vision
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key entex-adventure-vision `
    --platform-name-full "Entex Adventure Vision" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput advision -skip_gameinfo -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    advision

# ----------------------
# Entex Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key entex-handhelds-lcd `
    --platform-name-full "Entex Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems blastit ebaskb2 ebball ebball2 ebball3 ebknight efootb4 egalaxn2 einvader einvader2 einvaderc epacman2 epacman2r esbattle esoccer estargte eturtles mmarvin raisedvl

# ----------------------
# Epoch Game Pocket Computer
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key epoch-game-pocket-computer `
    --platform-name-full "Epoch Game Pocket Computer" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gamepock -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    gamepock

# ----------------------
# Epoch Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key epoch-handhelds-lcd `
    --platform-name-full "Epoch Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems alienfev astrocmd edracula efball einspace galaxy2 galaxy2b

# ----------------------
# Epoch Super Cassette Vision
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key epoch-super-cassette-vision `
    --platform-name-full "Epoch Super Cassette Vision" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput scv -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    scv

# ----------------------
# Epoch TV Games
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key epoch-tv-games `
    --platform-name-full "Epoch TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --fuzzy epo_

# ----------------------
# Epoch TV PC
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key epoch-tv-pc `
    --platform-name-full "Epoch TV PC" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --fuzzy tvpc_

# ----------------------
# Exelvision EXL 100
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key exelvision-exl-100 `
    --platform-name-full "Exelvision EXL 100" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput exl100 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    exl100

# ----------------------
# Funtech Super Acan
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key funtech-super-acan `
    --platform-name-full "Funtech Super Acan" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput supracan -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    supracan

# ----------------------
# Gakken Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key gakken-handhelds-lcd `
    --platform-name-full "Gakken Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems fxmcr165 gckong gdefender gdigdug ghalien ginv ginv1000 ginv2000 gjackpot gpoker gscobra gjungler

# ----------------------
# GamePark GP32
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key gamepark-gp32 `
    --platform-name-full "GamePark GP32" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gp32" `
    --output-format yaml `
    --output-file system_softlist.yml `
    gp32

# ----------------------
# Hartung Game Master
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key hartung-game-master `
    --platform-name-full "Hartung Game Master" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gmaster -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    gmaster

# ----------------------
# Hasbro TV Games
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key hasbro-tv-games `
    --platform-name-full "Hasbro TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems beambox dreamlif dsgnwrld gigapets parcade has_wamg dreamlss pballpup swclone

# ----------------------
# Interton VC 4000
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key interton-vc-4000 `
    --platform-name-full "Interton VC 4000" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vc4000 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    vc4000

# ----------------------
# JAKKS Pacific Telestory
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key jakks-pacific-telestory `
    --platform-name-full "JAKKS Pacific Telestory" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput telestry -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    telestry

# ----------------------
# JAKKS Pacific TV Game
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key jakks-pacific-tv-game `
    --platform-name-full "JAKKS Pacific TV Game" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --enable-custom-cmd-per-title `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --fuzzy jak `
    --exclude-systems jak_pf jak_prft jak_s500 jak_smwm jak_ths jak_tink jak_totm jak_umdf

# ----------------------
# JAKKS Pacific TV Motion Game
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key jakks-pacific-tv-motion-game `
    --platform-name-full "JAKKS Pacific TV Motion Game" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --enable-custom-cmd-per-title `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    jaks

# ----------------------
# JoyPalette TV Games
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key joypalette-tv-games `
    --platform-name-full "JoyPalette TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems anpanbd anpanm15 anpanm19 anpanmdx apmj2009

# ----------------------
# JungleTac Vii
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key jungletac-vii `
    --platform-name-full "JungleTac Vii" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vii -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    vii

# ----------------------
# Koei PasoGo
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key koei-pasogo `
    --platform-name-full "Koei PasoGo" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput pasogo -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    pasogo

# ----------------------
# Konami Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key konami-handhelds-lcd `
    --platform-name-full "Konami Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems kbilly kblades kbottom9 kbucky kchqflag kcontra kdribble kgarfld kgradius kloneran knascar knfl kskatedie kst25 ktmnt ktmnt2 ktmnt3 ktmntbb ktopgun ktopgun2

# ----------------------
# Lexibook TV Games
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key lexibook-tv-games `
    --platform-name-full "Lexibook TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems lexiart lexifit lexitvsprt lx_aven lx_frozen lx_jg7420 lx_jg7425 lxairjet lxspidaj lexizeus lx_jg7410 lx_jg7415 lexiseal

# ----------------------
# Mattel Electronics Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key mattel-electronics-handhelds-lcd `
    --platform-name-full "Mattel Electronics Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems autorace brainbaf funjacks funrlgl funtag gravity horocomp horseran lafootb mbaseb mbaskb mbaskb2 mcompgin mdallas mdndclab mfootb mfootb2 mhockey mhockeya misatk msoccer msoccer2 msthawk mwcbaseb mwcfootb

# ----------------------
# Mattel Intellivision ECS
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key mattel-intellivision-ecs `
    --platform-name-full "Mattel Intellivision ECS" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput intvecs -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    intvecs

# ----------------------
# Milton Bradley Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key milton-bradley-handhelds-lcd `
    --platform-name-full "Milton Bradley Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems arcmania bigtrak bship bshipb bshipg comp4 lightfgt mbdtower plus1 simon simonf ssimon

# ----------------------
# Nichibutsu My Vision
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key nichibutsu-my-vision `
    --platform-name-full "Nichibutsu My Vision" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput myvision -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    myvision

# ----------------------
# Nintendo FamicomBox
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key nintendo-famicombox `
    --platform-name-full "Nintendo FamicomBox" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput famibox" `
    --output-format yaml `
    --output-file system_softlist.yml `
    famibox

# ----------------------
# Nintendo Game & Watch
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key nintendo-game-and-watch `
    --platform-name-full "Nintendo Game & Watch" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --fuzzy gnw_

# ----------------------
# Nintendo Super Game Boy
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key nintendo-super-game-boy `
    --platform-name-full "Nintendo Super Game Boy" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems supergb supergb2

# ----------------------
# Parker Brothers Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key parker-brothers-handhelds-lcd `
    --platform-name-full "Parker Brothers Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems bankshot cnsector lostreas merlin mmerlin pbmastm pbqbert splitsec stopthief stopthiefp talkingbb talkingfb wildfire

# ----------------------
# Philips Videopac+
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key philips-videopac-plus `
    --platform-name-full "Philips Videopac+" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput videopac -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    videopac

# ----------------------
# Play Vision TV Games
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key play-vision-tv-games `
    --platform-name-full "Play Vision TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems pvmil pvmil8 pvmilfin pvwwcas

# ----------------------
# RADICA Play TV
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key radica-play-tv `
    --platform-name-full "RADICA Play TV" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --fuzzy rad_

# ----------------------
# RCA Studio II
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key rca-studio-ii `
    --platform-name-full "RCA Studio II" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput studio2 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    studio2

# ----------------------
# Sega Beena
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key sega-beena `
    --platform-name-full "Sega Beena" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput beena -cart1" `
    --output-format yaml `
    --output-file system_softlist.yml `
    beena

# ----------------------
# Sega SC-3000
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key sega-sc-3000 `
    --platform-name-full "Sega SC-3000" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput sc3000 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    sc3000

# ----------------------
# Senario TV Games
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key senario-tv-games `
    --platform-name-full "Senario TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems ddmmeg12 ddmsup drumsups gssytts guitarss guitarssa guitarst senapren senbbs sencosmo senmil senpmate senspeed senspid senstriv sentx6p sentx6pd senwfit totspies sentx6puk mysprtch mysprtcp mysptqvc

# ----------------------
# Sord M5
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key sord-m5 `
    --platform-name-full "Sord M5" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput m5 -cart1" `
    --output-format yaml `
    --output-file system_softlist.yml `
    m5

# ----------------------
# Spectravision SVI-318
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key spectravision-svi-318 `
    --platform-name-full "Spectravision SVI-318" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput svi318 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    svi318

# ----------------------
# Super Impulse TV Games
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key super-impulse-tv-games `
    --platform-name-full "Super Impulse TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems mapacman siddr tagalaga taspinv taturtf

# ----------------------
# Takara e-kara
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key takara-e-kara `
    --platform-name-full "Takara e-kara" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput ekaraa -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    ekaraa

# ----------------------
# Takara Jumping Popira
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key takara-jumping-popira `
    --platform-name-full "Takara Jumping Popira" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput jpopira -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    jpopira

# ----------------------
# Takara Popira
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key takara-popira `
    --platform-name-full "Takara Popira" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --enable-custom-cmd-per-title `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    popira

# ----------------------
# Takara Tomy TV Game
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key takara-tomy-tv-game `
    --platform-name-full "Takara Tomy TV Game" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --enable-custom-cmd-per-title `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --fuzzy tak_ `
    --include-systems duelmast gungunad gungunrv jarajal pocketmp pocketmr prail prailpls rizstals tmy_rkmj tomthr tomyegg tcarnavi tmy_thom tom_dpgm tom_jump tom_tvho tomcpin tomplc tomshoot ttv_swj tomycar

# ----------------------
# Tandy TRS-80 Color Computer
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key tandy-trs-80-color-computer `
    --platform-name-full "Tandy TRS-80 Color Computer" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput coco3h -cart1" `
    --output-format yaml `
    --output-file system_softlist.yml `
    coco3h

# ----------------------
# Technosys Aamber Pegasus
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key technosys-aamber-pegasus `
    --platform-name-full "Technosys Aamber Pegasus" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput pegasus" `
    --output-format yaml `
    --output-file system_softlist.yml `
    pegasus

# ----------------------
# Tiger Electronics Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key tiger-electronics-handhelds-lcd `
    --platform-name-full "Tiger Electronics Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems copycat copycata ditto dxfootb fingbowl hccbaskb rockpin rzbatfor rzindy500 rztoshden subwars t7in1ss taddams taltbeast tapollo13 tbatfor tbatman tbatmana tbtoads tbttf tddragon tddragon2 tddragon3 tdennis tdummies tflash tgaiden tgaiden3 tgargnf tgaunt tgoldeye tgoldnaxe thalone thalone2 thook tinday tjdredd tjpark tkarnov tkazaam tkkongq tlluke2 tmchammer tmegaman3 tmigmax tmkombat tnmarebc topaliens tpitfight trobhood trobocop2 trobocop3 trockteer tsddragon tsf2010 tsfight2 tshadow tsharr2 tsimquest tsjam tskelwarr tsonic tsonic2 tspidman tstrider tsuperman tswampt ttransf2 tvindictr twworld txmen txmenpx

# ----------------------
# Tiger Game.com
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key tiger-game-com `
    --platform-name-full "Tiger Game.com" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gamecom -cart1" `
    --output-format yaml `
    --output-file system_softlist.yml `
    gamecom

# ----------------------
# TimeTop Game King
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key timetop-game-king `
    --platform-name-full "TimeTop Game King" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gameking -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    gameking

# ----------------------
# TimeTop Game King 3
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key timetop-game-king-3 `
    --platform-name-full "TimeTop Game King 3" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gamekin3 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    gamekin3

# ----------------------
# Tomy evio
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key tomy-evio `
    --platform-name-full "Tomy evio" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput evio -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    evio

# ----------------------
# Tomy Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key tomy-handhelds-lcd `
    --platform-name-full "Tomy Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems alnchase bombman kingman phpball tbreakup tcaveman tccombat tmbaskb tmpacman tmscramb tmtennis tmtron tmvolleyb

# ----------------------
# Tomy Tutor
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key tomy-tutor `
    --platform-name-full "Tomy Tutor" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput tutor -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    tutor

# ----------------------
# Tronica Handhelds (LCD)
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key tronica-handhelds-lcd `
    --platform-name-full "Tronica Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems tigarden trclchick trdivadv trsgkeep trshutvoy trspacadv trspacmis trspider trsrescue trthuball

# ----------------------
# Ultimate Products TV Games
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key ultimate-products-tv-games `
    --platform-name-full "Ultimate Products TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems zone100 zone60 zon32bit rockstar react zone40 zonemini

# ----------------------
# Uzebox
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key uzebox `
    --platform-name-full "Uzebox" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput uzebox -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    uzebox

# ----------------------
# VideoBrain Family Computer
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key videobrain-family-computer `
    --platform-name-full "VideoBrain Family Computer" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vidbrain -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    vidbrain

# ----------------------
# Videoton TVC 64
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key videoton-tvc-64 `
    --platform-name-full "Videoton TVC 64" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput tvc64p -cart1" `
    --output-format yaml `
    --output-file system_softlist.yml `
    tvc64p

# ----------------------
# VTech Creativision
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key vtech-creativision `
    --platform-name-full "VTech Creativision" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput crvision -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    crvision

# ----------------------
# VTech Genius Leader Color
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key vtech-genius-leader-color `
    --platform-name-full "VTech Genius Leader Color" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput glcolor -cart1" `
    --output-format yaml `
    --output-file system_softlist.yml `
    glcolor

# ----------------------
# VTech Socrates
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key vtech-socrates `
    --platform-name-full "VTech Socrates" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput socrates -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    socrates

# ----------------------
# VTech TV Games
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key vtech-tv-games `
    --platform-name-full "VTech TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --include-systems doraglob doraglobf doraglobg doraphon doraphonf hippofr kidizmb kidizmp vtechtvsgr vtechtvssp

# ----------------------
# VTech VSmile
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key vtech-vsmile `
    --platform-name-full "VTech VSmile" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vsmile -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    vsmile

# ----------------------
# VTech VSmile Baby
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key vtech-vsmile-baby `
    --platform-name-full "VTech VSmile Baby" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vsmileb -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    vsmileb

# ----------------------
# VTech VSmile Motion
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key vtech-vsmile-motion `
    --platform-name-full "VTech VSmile Motion" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vsmilem -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    vsmilem

# ----------------------
# Watara Supervision
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key watara-supervision `
    --platform-name-full "Watara Supervision" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput svision -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    svision