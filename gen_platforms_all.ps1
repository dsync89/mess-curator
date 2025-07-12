# ----------------------
# Acorn Archimedes
# ----------------------
python .\src\mess_curator.py search `
    --platform-key acorn-archimedes `
    --platform-name-full "Acorn Archimedes" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput aa4401 -flop' `
    --output-format yaml `
    aa4401

# ----------------------
# Acorn Atom
# ----------------------
python .\src\mess_curator.py search `
    --platform-key acorn-atom `
    --platform-name-full "Acorn Atom" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput atom -autoboot_delay \"2\" -autoboot_command \"DOS\nCAT\n*RUN\"\" -flop1' `
    --output-format yaml `
    --include-softlist "atom_flop" `
    --add-software-config 'atom_flop:chuckie:atom -ab *DOS\n*CAT\n*RUN\"CCHUCK\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:egghead:atom -ab *DOS\n*CAT\n*RUN\"EHRUN\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:f14:atom -ab *DOS\n*CAT\n*RUN\"F14RUN\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:gala:atom -ab *DOS\n*CAT\n*RUN\"CGALA\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:galxians:atom -ab *DOS\n*CAT\n*RUN\"GALAXI\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:hardhath:atom -ab *DOS\n*CAT\n*RUN\"LOADER\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:hypervpr:atom -ab *DOS\n*CAT\n*RUN\"LOADER\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:jetsetmn:atom -ab *DOS\n*CAT\n*RUN\"LOADER\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:joeblade:atom -ab *DOS\n*CAT\n*RUN\"JOE\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:jsw:atom -ab *DOS\n*CAT\n*RUN\"JSWRUN\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:jsw2:atom -ab *DOS\n*CAT\n*RUN\"JSW2RUN\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:jungle:atom -ab *DOS\n*CAT\n*RUN\"JUNGLE\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:manicmin:atom -ab *DOS\n*CAT\n*RUN\"MMRUN\"\n -autoboot_delay 1 -flop1' `
    --add-software-config 'atom_flop:repton:atom -ab *DOS\n*CAT\n*RUN\"REPLOAD\"\n -autoboot_delay 1 -flop1' `
    atom

# ----------------------
# Acorn Electron
# ----------------------
python .\src\mess_curator.py search `
    --platform-key acorn-electron `
    --platform-name-full "Acorn Electron" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cass `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput electron -skip_gameinfo -autoboot_delay \"2\" -autoboot_command \"*tape\nchain\"\"\"\"\"\"\n\" -cass' `
    --output-format yaml `
    --exclude-softlist "electron_rom" `
    --add-softlist-config 'bbc_cass:electron -skip_gameinfo -autoboot_delay "2" -autoboot_command "*TAPE\nCHAIN\"\"\"\"\"\"\n" -cass' `
    --add-softlist-config 'electron_cass:electron -skip_gameinfo -autoboot_delay "2" -autoboot_command "*TAPE\nCHAIN\"\"\"\"\"\"\n" -cass' `
    --add-softlist-config 'electron_cart:electron -cart' `
    --add-softlist-config 'electron_flop:electron -skip_gameinfo -autoboot_delay "2" -autoboot_command \"cat\n\n\n\n\n\nrun !boot\n\" -flop' `
    electron

# ----------------------
# Amstrad CPC
# ----------------------
python .\src\mess_curator.py search `
    --platform-key amstrad-cpc `
    --platform-name-full "Amstrad CPC" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput cpc464 -flop1' `
    --output-format yaml `
    --include-softlist "cpc_cass" `
    --add-softlist-config 'cpc_cass:cpc464 -autoboot_delay 2 -autoboot_command LOAD\\\"\\\"\n -cass' `
    cpc464

# ----------------------
# Amstrad GX4000
# ----------------------
python .\src\mess_curator.py search `
    --platform-key amstrad-gx4000 `
    --platform-name-full "Amstrad GX4000" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gx4000 -cart" `
    --output-format yaml `
    --add-softlist-config 'gx4000:gx4000 -cart' `
    gx4000

# ----------------------
# Atari XEGS
# ----------------------
python .\src\mess_curator.py search `
    --platform-key atari-xegs `
    --platform-name-full "Atari XEGS" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput xegs -cart" `
    --output-format yaml `
    --exclude-softlist "a800 a800_cass a800_flop" `
    xegs

# ----------------------
# Bally Astrocade
# ----------------------
python .\src\mess_curator.py search `
    --platform-key bally-astrocade `
    --platform-name-full "Bally Astrocade" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput astrocde -cart" `
    --output-format yaml `
    --add-softlist-config 'astrocde:astrocde -cart' `
    astrocde

# ----------------------
# Bambino Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key bambino-handhelds-lcd `
    --platform-name-full "Bambino Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "bambball bmboxing bmcfball bmsafari bmsoccer splasfgt ssfball ufombs"

# ----------------------
# Bandai Gundam RX-78
# ----------------------
python .\src\mess_curator.py search `
    --platform-key bandai-gundam-rx-78 `
    --platform-name-full "Bandai Gundam RX-78" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput rx78 -cart" `
    --output-format yaml `
    --add-softlist-config 'rx78_cart:rx78 -cart' `
    --add-softlist-config 'rx78_cass:rx78 -cass1' `
    --add-software-config 'rx78_cass:graphmaths:rx78 -autoboot_delay 2 -autoboot_command MON\nL\nGRM\n -cart basic -cass1' `
    --add-software-config 'rx78_cass:yellowcab:rx78 -autoboot_delay 2 -autoboot_command MON\nL\nCAB\n -cart basic -cass1' `
    rx78

# ----------------------
# Bandai Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key bandai-handhelds-lcd `
    --platform-name-full "Bandai Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "bbtime bcclimbr bcheetah bdoramon bfriskyt bgalaxn bgunf bpengo bultrman bzaxxon ggdman ktparman machiman paccon packmon pairmtch racetime tc7atc tkjmaru uboat zackman"

# ----------------------
# Bandai Let's! TV Play
# ----------------------
python .\src\mess_curator.py search `
    --platform-key bandai-lets-tv-play `
    --platform-name-full "Bandai Let's! TV Play" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --fuzzy ban_ `
    --include-systems "anpantv dmbtjunc dmnslayg paccon ltv_naru ltv_tam maxheart mrangbat namcons1 namcons2 taitons1 taitons2"


# ----------------------
# Bandai Super Note Club
# ----------------------
python .\src\mess_curator.py search `
    --platform-key bandai-super-note-club `
    --platform-name-full "Bandai Super Note Club" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput snotec -cart" `
    --output-format yaml `
    --add-softlist-config 'glcolor:snotec -cart' `
    --add-softlist-config 'snotec:snotec -cart' `
    snotec

# ----------------------
# Bandai Super Vision 8000
# ----------------------
python .\src\mess_curator.py search `
    --platform-key bandai-super-vision-8000 `
    --platform-name-full "Bandai Super Vision 8000" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput sv8000 -cart1" `
    --output-format yaml `
    --add-softlist-config 'sv8000:sv8000 -cart1' `
    sv8000

# ----------------------
# Bandai Tamagotchi
# ----------------------
python .\src\mess_curator.py search `
    --platform-key bandai-tamagotchi `
    --platform-name-full "Bandai Tamagotchi" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "digimon digimonv2 digimonv3 tama tamaang tamag2 tamamot tamapix tamamot"

# ----------------------
# BBC Microcomputer System
# ----------------------
python .\src\mess_curator.py search `
--platform-key bbc-microcomputer-system `
--platform-name-full "BBC Microcomputer System" `
--platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
--media-type floppy `
--emu-name "MAME (MESS)" `
--default-emu `
--default-emu-cmd-params '-keyboardprovider dinput bbcb -skip_gameinfo -flop1' `
--output-format yaml `
--exclude-softlist "bbc_rom bbc_hdd" `
--add-softlist-config 'bbcb_flop:bbcb -skip_gameinfo -autoboot_delay "1" -autoboot_command \"*cat\n*exec !boot\n\" -flop1' `
--add-softlist-config 'bbcb_flop_orig:bbcb -skip_gameinfo -autoboot_delay "1" -autoboot_command \"*cat\n*exec !boot\n\" -flop1' `
bbcb

# ----------------------
# Bit Corp Gamate
# ----------------------
python .\src\mess_curator.py search `
    --platform-key bit-corp-gamate `
    --platform-name-full "Bit Corp Gamate" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gamate -cart" `
    --output-format yaml `
    gamate

# ----------------------
# Camputers Lynx
# ----------------------
python .\src\mess_curator.py search `
    --platform-key camputers-lynx `
    --platform-name-full "Camputers Lynx" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput lynx128k -autoboot_delay \"2\" -autoboot_command \"XROM\n\n\nEXT DIR\n\n\n\n\n\n\n\nEXT LOAD \"\" -flop1' `
    --output-format yaml `
    --add-softlist-config 'camplynx_cass:lynx128k -skip_gameinfo -autoboot_delay "1" -autoboot_command \"mload\"\"\"\"\"\"\n\" -cass' `
    --add-softlist-config 'camplynx_flop:lynx128k -skip_gameinfo -autoboot_delay "1" -autoboot_command \"*cat\n*exec !boot\n\" -flop1' `
    --add-software-config 'camplynx_cass:3dmoncrz:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"3D MONSTER\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:backgmmn:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"BACKGAMMON\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:battlbrk:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"BATTLEBRICK\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:centiped:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"CENTIPEDE\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:colossal:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"COLOSSAL\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:dambustr:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"DAM BUSTER\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:deathball:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"DEATHBALL\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:diggerman:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"DIGGERMAN\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:dungeon:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"DUNGEON\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:floydbank:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"FLOYDS BANK\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:gamepak4:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"GEMPACK 4\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:gobblspk:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"SPOOK\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:hangman:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"HANGMAN\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:labyrinth:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"LABYRINTHE\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:logichess:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"ECHECS\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:invaders:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"INVADERS\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:mastermnd:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"MASTERMIND\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:mazeman:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"MAZEMAN\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:minedout:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"MINEDOUTGOOD\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:moonfallf:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"Moonfall2\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:moonfall:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"MOONFALL\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:muncher:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"MUNCHER\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:nuclear:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"NUCLEAR\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:numerons:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"NUMERONS\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:asterix:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"ASTERIX\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:ohmummy:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"OH MUMMY\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:panik:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"PANIK\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:pengo:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"PENGO\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:pwrblastr:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"POWER BLASTER\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:racer:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"RACER\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:rocketman:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"ROCKETMAN\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:spellbnd:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"SPELLBOUND\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:scrablynx:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"SCRABLYNX\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:siege:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"SIEGE ATTACK\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:spactrek:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"TREK\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:sairraid:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"SUPER AIR RAID\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:treasisld:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"TREASURE\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:twinkle:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"TWINKLE\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:worm:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"THE WORM\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:wormf:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"THE WORM\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:ynxvader:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"YNXVADERS\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:zombie:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"ZombiePanic\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:aide:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"AIDE\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:cardindx:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"CARD INDEX\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:composer:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"COMPOSER\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:disassmbf:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"DES.IMP\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:disassmb:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"DESASS\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:genbasic:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"GENEBASIC\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:gencarac:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"GENECAR\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:wordproc:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"LIONTEXT\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:moder80:lynx128k -autoboot_delay 2 -autoboot_command \"MLOAD \\\"CODE\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:musicmstr:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"MUSIC MASTER\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:6845p:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"6845P\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:chopin:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"CHOPIN\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:cinema:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"CINEMA\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:forest:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"THE FOREST\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:gridtrap:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"GRIDTRAP\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:hilo:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"CARDS\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:inteltab:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"INTELTABLYNX\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:maximots:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"MAXI-MOTS\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:planets:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"PLANETS\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:risingmn:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"CP FP\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:scrndmp:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"RPENROSE\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:starover:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"SR\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:triangle:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"BRUMBELOW\\\"\n\" -cass' `
    --add-software-config 'camplynx_cass:tronblkr:lynx128k -autoboot_delay 2 -autoboot_command \"LOAD \\\"TRON BLOCKER\\\"\n\" -cass' `
    --add-software-config 'camplynx_flop:bttlships:lynx128k -autoboot_delay 2 -autoboot_command \"EXT LOAD \\\"BATTLESHIPS\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:deltawng:lynx128k -autoboot_delay 2 -autoboot_command \"EXT LOAD \\\"DW.L\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:gomoku:lynx128k -autoboot_delay 2 -autoboot_command \"EXT LOAD \\\"GOMOKU\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:hangman:lynx128k -autoboot_delay 2 -autoboot_command \"EXT LOAD \\\"HANGMAN\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:intro128:lynx128k -autoboot_delay 2 -autoboot_command \"EXT LOAD \\\"INTRO128\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:logichess:lynx128k -autoboot_delay 2 -autoboot_command \"EXT MLOAD \\\"LC2.2\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:mnstrmine:lynx128k -autoboot_delay 2 -autoboot_command \"EXT MLOAD \\\"MONSTERMINE\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:roader:lynx128k -autoboot_delay 2 -autoboot_command \"EXT MLOAD \\\"ROADER\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:slot:lynx128k -autoboot_delay 2 -autoboot_command \"EXT LOAD \\\"SLOT\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:treasisld:lynx128k -autoboot_delay 2 -autoboot_command \"EXT LOAD \\\"TREASUREISLAND\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:forth:lynx128k -autoboot_delay 2 -autoboot_command \"EXT MLOAD \\\"FORTH\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:lrg1:lynx128k -autoboot_delay 2 -autoboot_command \"EXT LOAD \\\"MENU\\\"\n\" -flop1' `
    --add-software-config 'camplynx_flop:calcstar:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:cobol:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:cpm22b10:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:cpm22b12:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:ccomp:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:datastar:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:dbase2:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:ebasic:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:fortran:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:mbasic:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:peachcalc:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:rptstar:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:tpascal:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:wordmstr:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    --add-software-config 'camplynx_flop:wordstar:lynx128k -autoboot_delay 2 -autoboot_command \"EXT BOOT\n\" -flop1' `
    lynx128k

# ----------------------
# Casio Loopy
# ----------------------
python .\src\mess_curator.py search `
    --platform-key casio-loopy `
    --platform-name-full "Casio Loopy" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput casloopy -cart" `
    --output-format yaml `
    casloopy

# ----------------------
# Casio PV-1000
# ----------------------
python .\src\mess_curator.py search `
    --platform-key casio-pv-1000 `
    --platform-name-full "Casio PV-1000" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput pv1000 -cart" `
    --output-format yaml `
    pv1000

# ----------------------
# Casio PV-2000
# ----------------------
python .\src\mess_curator.py search `
    --platform-key casio-pv-2000 `
    --platform-name-full "Casio PV-2000" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput pv2000 -cart" `
    --output-format yaml `
    --add-softlist-config 'pv2000:pv2000 -cart' `
    pv2000

# ----------------------
# Coleco ADAM
# ----------------------
python .\src\mess_curator.py search `
    --platform-key coleco-adam `
    --platform-name-full "Coleco ADAM" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput adam -skip_gameinfo -flop1' `
    --output-format yaml `
    --exclude-softlist "adam_cart coleco coleco_homebrew" `
    --add-softlist-config 'adam_cass:adam -skip_gameinfo -cass1' `
    --add-softlist-config 'adam_flop:adam -skip_gameinfo -flop1' `
    adam

# ----------------------
# Coleco Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key coleco-handhelds-lcd `
    --platform-name-full "Coleco Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "alnattck amaztron cdkong cgalaxn cmspacmn cpacman cpacmanr1 cqback cfrogger"

# ----------------------
# Commodore VIC-10
# ----------------------
python .\src\mess_curator.py search `
    --platform-key commodore-vic-10 `
    --platform-name-full "Commodore VIC-10" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vic10 -cart" `
    --output-format yaml `
    --add-softlist-config 'vic10:vic10 -cart' `
    vic10

# ----------------------
# Commodore VIC-20
# ----------------------
python .\src\mess_curator.py search `
    --platform-key commodore-vic-20 `
    --platform-name-full "Commodore VIC-20" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vic1001 -cart" `
    --output-format yaml `
    --exclude-softlist "vic1001_cass vic1001_flop " `
    --add-softlist-config 'vic1001_cart:vic1001 -cart' `
    vic1001

# ----------------------
# Conny TV Games
# ----------------------
python .\src\mess_curator.py search `
    --platform-key conny-tv-games `
    --platform-name-full "Conny TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "conyteni pdc100 conyfght conyping dorapdc pdc150t pdc200 pdc40t pdc50 tmntpdc vjpp2"

# ----------------------
# Creatronic Mega Duck
# ----------------------
python .\src\mess_curator.py search `
    --platform-key creatronic-mega-duck `
    --platform-name-full "Creatronic Mega Duck" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput megaduck -cart" `
    --output-format yaml `
    megaduck

# ----------------------
# Dick Smith Super-80
# ----------------------
python .\src\mess_curator.py search `
    --platform-key dick-smith-super-80 `
    --platform-name-full "Dick Smith Super-80" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput super80 -cass" `
    --output-format yaml `
    --add-softlist-config 'super80_cass:super80 -skip_gameinfo -cass' `
    super80

# ----------------------
# Dick Smith Super-80 (VDUEB)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key dick-smith-super-80-vdueb `
    --platform-name-full "Dick Smith Super-80 (VDUEB)" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput super80v -cass" `
    --output-format yaml `
    --add-softlist-config 'super80_cass:super80v -skip_gameinfo -cass' `
    --add-softlist-config 'super80_flop:super80v -skip_gameinfo -flop' `
    super80v

# ----------------------
# Dragon
# ----------------------
python .\src\mess_curator.py search `
    --platform-key dragon `
    --platform-name-full "Dragon" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput dragon64 -cart" `
    --output-format yaml `
    --exclude-softlist "dragon_flex dragon_flop dragon_os9" `
    --add-softlist-config 'coco_cart:dragon64 -skip_gameinfo -cart' `
    --add-softlist-config 'dragon_cart:dragon64 -skip_gameinfo -cart' `
    --add-softlist-config 'dragon_cass:dragon64 -skip_gameinfo -autoboot_delay 4 -autoboot_command CLOAD\n -cass' `
    dragon64

# ----------------------
# EACA EG2000 Colour Genie
# ----------------------
python .\src\mess_curator.py search `
    --platform-key eaca-eg2000-colour-genie `
    --platform-name-full "EACA EG2000 Colour Genie" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput cgenie -autoboot_command \n\nCLOAD\n -autoboot_delay 1 -cass' `
    --output-format yaml `
    --add-softlist-config 'cgenie_cass:cgenie -autoboot_command \n\nCLOAD\n -autoboot_delay 1 -ram 32k -cass' `
    cgenie

# ----------------------
# Emerson Arcadia 2001
# ----------------------
python .\src\mess_curator.py search `
    --platform-key emerson-arcadia-2001 `
    --platform-name-full "Emerson Arcadia 2001" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput arcadia -cart" `
    --output-format yaml `
    arcadia

# ----------------------
# Entex Adventure Vision
# ----------------------
python .\src\mess_curator.py search `
    --platform-key entex-adventure-vision `
    --platform-name-full "Entex Adventure Vision" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput advision -skip_gameinfo -cart" `
    --output-format yaml `
    advision

# ----------------------
# Entex Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key entex-handhelds-lcd `
    --platform-name-full "Entex Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "blastit ebaskb2 ebball ebball2 ebball3 ebknight efootb4 egalaxn2 einvader einvader2 einvaderc epacman2 epacman2r esbattle esoccer estargte eturtles mmarvin raisedvl"

# ----------------------
# Epoch Game Pocket Computer
# ----------------------
python .\src\mess_curator.py search `
    --platform-key epoch-game-pocket-computer `
    --platform-name-full "Epoch Game Pocket Computer" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gamepock -cart" `
    --output-format yaml `
    gamepock

# ----------------------
# Epoch Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key epoch-handhelds-lcd `
    --platform-name-full "Epoch Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "alienfev astrocmd edracula efball einspace galaxy2 galaxy2b"

# ----------------------
# Epoch Super Cassette Vision
# ----------------------
python .\src\mess_curator.py search `
    --platform-key epoch-super-cassette-vision `
    --platform-name-full "Epoch Super Cassette Vision" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput scv -cart" `
    --output-format yaml `
    scv

# ----------------------
# Epoch TV Games
# ----------------------
python .\src\mess_curator.py search `
    --platform-key epoch-tv-games `
    --platform-name-full "Epoch TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --fuzzy epo_

# ----------------------
# Epoch TV PC
# ----------------------
python .\src\mess_curator.py search `
    --platform-key epoch-tv-pc `
    --platform-name-full "Epoch TV PC" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --fuzzy tvpc_

# ----------------------
# Exelvision EXL 100
# ----------------------
python .\src\mess_curator.py search `
    --platform-key exelvision-exl-100 `
    --platform-name-full "Exelvision EXL 100" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput exl100 -cart" `
    --output-format yaml `
    --add-softlist-config 'exl100:exl100 -cart' `
    exl100

# ----------------------
# Exidy Sorcerer
# ----------------------
python .\src\mess_curator.py search `
    --platform-key exidy-sorcerer `
    --platform-name-full "Exidy Sorcerer" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput sorcerer2 -autoboot_command \"LOG\n\" -autoboot_delay 3 -cass1' `
    --output-format yaml `
    --add-softlist-config 'sorcerer_cart:sorcerer2 -cart' `
    --add-softlist-config 'sorcerer_cass:sorcerer2 -autoboot_delay 3 -autoboot_command CLOAD\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:adv1:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:adv2:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:adv3:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:adv4:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:adv5:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:adv6:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:adv7:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:adv8:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:adv9:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:amaze:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:apatrol:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:arith:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:arrow:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:arrow2:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:ast:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:aster:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:astro:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:atc:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:atc1:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:biochart:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:biorhythm:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:blackj:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:cadas:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:char:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:chess1:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:chess2:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:chomp:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:com48:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:cosmc:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:crash:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:debug:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:defcm:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:dfndr:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:disas2:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:dterm:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:dybug:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:ezy:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:fgam:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:flip:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:flite:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:galax:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:galx:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:grotnik:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:homerun:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:hpad:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:interceptor:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:invad2:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:invaders:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:kalid:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:kilo:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:kilopede:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:killerg:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:l2x:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:landarc:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:ldg:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:magicmaze:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:midas:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:minva:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:misil:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:mmind:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:munch:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:nike2:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:robot:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:spider:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:starf:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:sword:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:wumpus:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    --add-software-config 'sorcerer_cass:zetu:sorcerer2 -autoboot_delay 4 -autoboot_command BYE\nLOG\n -cart basicpac -cass1' `
    sorcerer2

# ----------------------
# Funtech Super Acan
# ----------------------
python .\src\mess_curator.py search `
    --platform-key funtech-super-acan `
    --platform-name-full "Funtech Super Acan" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput supracan -cart" `
    --output-format yaml `
    supracan

# ----------------------
# Gakken Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key gakken-handhelds-lcd `
    --platform-name-full "Gakken Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "fxmcr165 gckong gdefender gdigdug ghalien ginv ginv1000 ginv2000 gjackpot gpoker gscobra gjungler"

# ----------------------
# GamePark GP32
# ----------------------
python .\src\mess_curator.py search `
    --platform-key gamepark-gp32 `
    --platform-name-full "GamePark GP32" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gp32" `
    --output-format yaml `
    gp32

# ----------------------
# Hartung Game Master
# ----------------------
python .\src\mess_curator.py search `
    --platform-key hartung-game-master `
    --platform-name-full "Hartung Game Master" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gmaster -cart" `
    --output-format yaml `
    gmaster

# ----------------------
# Hasbro TV Games
# ----------------------
python .\src\mess_curator.py search `
    --platform-key hasbro-tv-games `
    --platform-name-full "Hasbro TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "beambox dreamlif dsgnwrld gigapets parcade has_wamg dreamlss pballpup swclone"

# ----------------------
# Interton VC 4000
# ----------------------
python .\src\mess_curator.py search `
    --platform-key interton-vc-4000 `
    --platform-name-full "Interton VC 4000" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vc4000 -cart" `
    --output-format yaml `
    vc4000

# ----------------------
# JAKKS Pacific Telestory
# ----------------------
python .\src\mess_curator.py search `
    --platform-key jakks-pacific-telestory `
    --platform-name-full "JAKKS Pacific Telestory" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput telestry -cart" `
    --output-format yaml `
    telestry

# ----------------------
# JAKKS Pacific TV Game
# ----------------------
python .\src\mess_curator.py search `
    --platform-key jakks-pacific-tv-game `
    --platform-name-full "JAKKS Pacific TV Game" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --enable-custom-cmd-per-title `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --fuzzy jak `
    --exclude-systems "jak_pf jak_prft jak_s500 jak_smwm jak_ths jak_tink jak_totm jak_umdf jakks_gamekey_rom_i2c_24lc04 jakks_gamekey_rom_i2c_base jakks_gamekey_rom_plain jakks_gamekey_slot"

# ----------------------
# JAKKS Pacific TV Motion Game
# ----------------------
python .\src\mess_curator.py search `
    --platform-key jakks-pacific-tv-motion-game `
    --platform-name-full "JAKKS Pacific TV Motion Game" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --enable-custom-cmd-per-title `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "jak_pf jak_prft jak_s500 jak_smwm jak_ths jak_tink jak_totm jak_umdf"

# ----------------------
# JoyPalette TV Games
# ----------------------
python .\src\mess_curator.py search `
    --platform-key joypalette-tv-games `
    --platform-name-full "JoyPalette TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "anpanbd anpanm15 anpanm19 anpanmdx apmj2009"

# ----------------------
# JungleTac Vii
# ----------------------
python .\src\mess_curator.py search `
    --platform-key jungletac-vii `
    --platform-name-full "JungleTac Vii" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vii -cart" `
    --output-format yaml `
    vii

# ----------------------
# Koei PasoGo
# ----------------------
python .\src\mess_curator.py search `
    --platform-key koei-pasogo `
    --platform-name-full "Koei PasoGo" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput pasogo -cart" `
    --output-format yaml `
    pasogo

# ----------------------
# Konami Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key konami-handhelds-lcd `
    --platform-name-full "Konami Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "kbilly kblades kbottom9 kbucky kchqflag kcontra kdribble kgarfld kgradius kloneran knascar knfl kskatedie kst25 ktmnt ktmnt2 ktmnt3 ktmntbb ktopgun ktopgun2"

# ----------------------
# Lexibook TV Games
# ----------------------
python .\src\mess_curator.py search `
    --platform-key lexibook-tv-games `
    --platform-name-full "Lexibook TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "lexiart lexifit lexitvsprt lx_aven lx_frozen lx_jg7420 lx_jg7425 lxairjet lxspidaj lexizeus lx_jg7410 lx_jg7415 lexiseal"

# ----------------------
# Matra & Hachette Alice 90
# ----------------------
python .\src\mess_curator.py search `
    --platform-key matra-hachette-alice-90 `
    --platform-name-full "Matra and Hachette Alice 90" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput alice90 -skip_gameinfo -autoboot_command "cload\n" -cass' `
    --output-format yaml `
    --add-softlist-config 'alice32:alice90 -skip_gameinfo -autoboot_delay 2 -autoboot_command "cload\n" -cass' `
    --add-softlist-config 'alice90:alice90 -skip_gameinfo -autoboot_delay 2 -autoboot_command "cload\n" -cass' `
    alice90


# ----------------------
# Mattel Electronics Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key mattel-electronics-handhelds-lcd `
    --platform-name-full "Mattel Electronics Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "autorace brainbaf funjacks funrlgl funtag gravity horocomp horseran lafootb mbaseb mbaskb mbaskb2 mcompgin mdallas mdndclab mfootb mfootb2 mhockey mhockeya misatk msoccer msoccer2 msthawk mwcbaseb mwcfootb"

# ----------------------
# Mattel Hyperscan
# ----------------------
python .\src\mess_curator.py search `
    --platform-key mattel-hyperscan `
    --platform-name-full "Mattel Hyperscan" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cdrom `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput hyprscan -cdrom' `
    --output-format yaml `
    --exclude-softlist "hyperscan_card" `
    hyprscan

# ----------------------
# Mattel Intellivision ECS
# ----------------------
python .\src\mess_curator.py search `
    --platform-key mattel-intellivision-ecs `
    --platform-name-full "Mattel Intellivision ECS" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput intvecs -cart" `
    --output-format yaml `
    intvecs
    
# ----------------------
# Memotech MTX
# ----------------------
python .\src\mess_curator.py search `
    --platform-key memotech-mtx `
    --platform-name-full "Memotech MTX" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput mtx512 -skip_gameinfo -autoboot_command "load\"\"\"\"\"\"\n" -autoboot_delay 3 -cass' `
    --output-format yaml `
    --include-softlist "mtx_cass" `
    --add-softlist-config 'mtx_cass:mtx512 -skip_gameinfo -autoboot_command "load\"\"\"\"\"\"\n" -autoboot_delay 3 -cass' `
    mtx512

# ----------------------
# Milton Bradley Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key milton-bradley-handhelds-lcd `
    --platform-name-full "Milton Bradley Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "arcmania bigtrak bship bshipb bshipg comp4 lightfgt mbdtower plus1 simon simonf ssimon"

# ----------------------
# Nichibutsu My Vision
# ----------------------
python .\src\mess_curator.py search `
    --platform-key nichibutsu-my-vision `
    --platform-name-full "Nichibutsu My Vision" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput myvision -cart" `
    --output-format yaml `
    myvision

# ----------------------
# Nintendo FamicomBox
# ----------------------
python .\src\mess_curator.py search `
    --platform-key nintendo-famicombox `
    --platform-name-full "Nintendo FamicomBox" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    famibox

# ----------------------
# Nintendo Game & Watch
# ----------------------
python .\src\mess_curator.py search `
    --platform-key nintendo-game-and-watch `
    --platform-name-full "Nintendo Game & Watch" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --fuzzy gnw_

# ----------------------
# Nintendo Super Game Boy
# ----------------------
python .\src\mess_curator.py search `
    --platform-key nintendo-super-game-boy `
    --platform-name-full "Nintendo Super Game Boy" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "supergb supergb2"

# ----------------------
# Parker Brothers Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key parker-brothers-handhelds-lcd `
    --platform-name-full "Parker Brothers Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "bankshot cnsector lostreas merlin mmerlin pbmastm pbqbert splitsec stopthief stopthiefp talkingbb talkingfb wildfire"


# ----------------------
# Philips VG 5000
# ----------------------
python .\src\mess_curator.py search `
    --platform-key philips-vg-5000 `
    --platform-name-full "Philips VG 5000" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput vg5k -skip_gameinfo -autoboot_command "cload\n" -autoboot_delay 3 -cass' `
    --output-format yaml `
    vg5k

# ----------------------
# Philips Videopac+
# ----------------------
python .\src\mess_curator.py search `
    --platform-key philips-videopac-plus `
    --platform-name-full "Philips Videopac+" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput videopac -cart" `
    --output-format yaml `
    videopac

# ----------------------
# Play Vision TV Games
# ----------------------
python .\src\mess_curator.py search `
    --platform-key play-vision-tv-games `
    --platform-name-full "Play Vision TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "pvmil pvmil8 pvmilfin pvwwcas"

# ----------------------
# RADICA Play TV
# ----------------------
python .\src\mess_curator.py search `
    --platform-key radica-play-tv `
    --platform-name-full "RADICA Play TV" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --fuzzy rad_

# ----------------------
# RCA Studio II
# ----------------------
python .\src\mess_curator.py search `
    --platform-key rca-studio-ii `
    --platform-name-full "RCA Studio II" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput studio2 -cart" `
    --output-format yaml `
    studio2

# ----------------------
# SAM Coupe
# ----------------------
python .\src\mess_curator.py search `
    --platform-key sam-coupe `
    --platform-name-full "SAM Coupe" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput samcoupe -autoboot_delay 2 -skip_gameinfo -autoboot_command \"\nBOOT\n\" -flop1' `
    --output-format yaml `
    --exclude-softlist "samcoupe_cass" `
    --add-softlist-config 'samcoupe_flop:samcoupe -autoboot_delay 2 -skip_gameinfo -autoboot_command "\nBOOT\n" -flop1' `
    samcoupe

# ----------------------
# Sega Beena
# ----------------------
python .\src\mess_curator.py search `
    --platform-key sega-beena `
    --platform-name-full "Sega Beena" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput beena -cart1" `
    --output-format yaml `
    beena

# ----------------------
# Sega SC-3000
# ----------------------
python .\src\mess_curator.py search `
    --platform-key sega-sc-3000 `
    --platform-name-full "Sega SC-3000" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput sc3000 -cart" `
    --output-format yaml `
    --exclude-softlist "sg1000" `
    --add-softlist-config 'sc3000_cart:sc3000 -cart' `
    --add-softlist-config 'sc3000_cass:sc3000 -cart basic3e -autoboot_delay 6 -autoboot_command "LOAD\nRUN"' `
    sc3000

# ----------------------
# Senario TV Games
# ----------------------
python .\src\mess_curator.py search `
    --platform-key senario-tv-games `
    --platform-name-full "Senario TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "ddmmeg12 ddmsup drumsups gssytts guitarss guitarssa guitarst senapren senbbs sencosmo senmil senpmate senspeed senspid senstriv sentx6p sentx6pd senwfit totspies sentx6puk mysprtch mysprtcp mysptqvc"

# ----------------------
# Sharp MZ-2500
# ----------------------
python .\src\mess_curator.py search `
    --platform-key sharp-mz-2500 `
    --platform-name-full "Sharp MZ-2500" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput mz2500 -flop1' `
    --output-format yaml `
    --exclude-softlist "mz2000_flop" `
    --add-softlist-config 'mz2500_flop:mz2500 -flop1' `
    mz2500

# ----------------------
# Sord M5
# ----------------------
python .\src\mess_curator.py search `
    --platform-key sord-m5 `
    --platform-name-full "Sord M5" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput m5 -cart1" `
    --output-format yaml `
    --add-softlist-config 'm5_cart:m5 -cart1' `
    --add-softlist-config 'm5_cass:m5 -autoboot_delay 3 -autoboot_command "CHAIN\n" -cart1 basici -cass' `
    m5

# ----------------------
# Spectravision SVI-318
# ----------------------
python .\src\mess_curator.py search `
    --platform-key spectravision-svi-318 `
    --platform-name-full "Spectravision SVI-318" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput svi318 -cart" `
    --output-format yaml `
    --add-softlist-config 'svi318_cart:svi318 -cart1' `
    --add-softlist-config 'svi318_cass:svi318 -autoboot_delay 3 -autoboot_command "CLOAD\n" -cass' `
    svi328

# ----------------------
# Super Impulse TV Games
# ----------------------
python .\src\mess_curator.py search `
    --platform-key super-impulse-tv-games `
    --platform-name-full "Super Impulse TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "mapacman siddr tagalaga taspinv taturtf"

# ----------------------
# Takara e-kara
# ----------------------
python .\src\mess_curator.py search `
    --platform-key takara-e-kara `
    --platform-name-full "Takara e-kara" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput ekaraa -cart" `
    --output-format yaml `
    ekaraa

# ----------------------
# Takara Jumping Popira
# ----------------------
python .\src\mess_curator.py search `
    --platform-key takara-jumping-popira `
    --platform-name-full "Takara Jumping Popira" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput jpopira -cart" `
    --output-format yaml `
    jpopira

# ----------------------
# Takara Popira
# ----------------------
python .\src\mess_curator.py search `
    --platform-key takara-popira `
    --platform-name-full "Takara Popira" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --enable-custom-cmd-per-title `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput popira -cart" `
    --output-format yaml `
    popira

# ----------------------
# Takara Tomy TV Game
# ----------------------
python .\src\mess_curator.py search `
    --platform-key takara-tomy-tv-game `
    --platform-name-full "Takara Tomy TV Game" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --enable-custom-cmd-per-title `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --fuzzy tak_ `
    --include-systems "duelmast gungunad gungunrv jarajal pocketmp pocketmr prail prailpls rizstals tmy_rkmj tomthr tomyegg tcarnavi tmy_thom tom_dpgm tom_jump tom_tvho tomcpin tomplc tomshoot ttv_swj tomycar"
    
# ----------------------
# Tandy Memorex VIS
# ----------------------
python .\src\mess_curator.py search `
    --platform-key tandy-memorex-vis `
    --platform-name-full "Tandy Memorex VIS" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cdrom `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput vis -cdrom' `
    --output-format yaml `
    vis

# ----------------------
# Tandy TRS-80
# ----------------------
python .\src\mess_curator.py search `
    --platform-key tandy-trs-80 `
    --platform-name-full "Tandy TRS-80" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput trs80 -cass' `
    --output-format yaml `
    --include-softlist "trs80_cass" `
    --add-software-config 'trs80_cass:adv03:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nMISSIO\n" -cass' `
    --add-software-config 'trs80_cass:adv10:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nSAVAGE\n" -cass' `
    --add-software-config 'trs80_cass:android:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:baccarat:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:backgamm:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:blakjack:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:chess:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nSARGON\n" -cass' `
    --add-software-config 'trs80_cass:colliss:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:cosmic:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nCOSMIC\n" -cass' `
    --add-software-config 'trs80_cass:craps:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:dddd:trs80m4 -autoboot_delay 2 -autoboot_command "\n\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nDANDEM\n" -cass' `
    --add-software-config 'trs80_cass:defense:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nDEFENS\n" -cass' `
    --add-software-config 'trs80_cass:dtrap:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"32640\nCLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:eliza:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nELIZA\n" -cass' `
    --add-software-config 'trs80_cass:env:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nENV\n" -cass' `
    --add-software-config 'trs80_cass:escape:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nESCAPE\n" -cass' `
    --add-software-config 'trs80_cass:galaxy1:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nGALAXY\n" -cass' `
    --add-software-config 'trs80_cass:galaxy2:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nGALAXY\n" -cass' `
    --add-software-config 'trs80_cass:headon:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nHEADON\n" -cass' `
    --add-software-config 'trs80_cass:heliko:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nHELIKO\n" -cass' `
    --add-software-config 'trs80_cass:hoppy:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nHG\n" -cass' `
    --add-software-config 'trs80_cass:invaders:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nINVADE\n" -cass' `
    --add-software-config 'trs80_cass:invasion:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nINVADE\n" -cass' `
    --add-software-config 'trs80_cass:keno:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:kinghill:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nR\n" -cass' `
    --add-software-config 'trs80_cass:meteor2:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nMETEOR\n" -cass' `
    --add-software-config 'trs80_cass:microply:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:penetr:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nPENETR\n" -cass' `
    --add-software-config 'trs80_cass:pinball:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:pyrmd:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nPYRMD\n" -cass' `
    --add-software-config 'trs80_cass:robot:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nROBOT\n" -cass' `
    --add-software-config 'trs80_cass:qwatson:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:roulette:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:scarfman:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nSCARFM\n" -cass' `
    --add-software-config 'trs80_cass:scripsit:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nSCRIPS\n" -cass' `
    --add-software-config 'trs80_cass:seadragon:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nSEADRA\n" -cass' `
    --add-software-config 'trs80_cass:slot:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:spaceinv:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nINVADE\n" -cass' `
    --add-software-config 'trs80_cass:spcinv:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nSPCINV\n" -cass' `
    --add-software-config 'trs80_cass:spcwarp:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nSPWAR\n" -cass' `
    --add-software-config 'trs80_cass:starfi:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nSTARFI\n" -cass' `
    --add-software-config 'trs80_cass:starsm:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nSTARSM\n" -cass' `
    --add-software-config 'trs80_cass:startrek:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:starwar:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:swamp:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nSWAMP\n" -cass' `
    --add-software-config 'trs80_cass:taipan:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:taxi:trs80m4 -autoboot_delay 2 -autoboot_command "\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nTAXI\n" -cass' `
    --add-software-config 'trs80_cass:trollcru:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:ulcbas:trs80m4 -autoboot_delay 2 -autoboot_command "\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nULCBAS\n" -cass' `
    --add-software-config 'trs80_cass:wheel:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"CLOAD\nRUN\n" -cass' `
    --add-software-config 'trs80_cass:zchess:trs80m4 -autoboot_delay 2 -autoboot_command "L\n\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"\\\"SYSTEM\nZCHESS\n" -cass' `
    trs80m4
    
# ----------------------
# Tandy TRS-80 Color Computer
# ----------------------
python .\src\mess_curator.py search `
    --platform-key tandy-trs-80-color-computer `
    --platform-name-full "Tandy TRS-80 Color Computer" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput coco3h -cart1" `
    --output-format yaml `
    --add-softlist-config 'coco_cart:coco3h -cart' `
    --add-softlist-config 'coco_flop:coco3h -flop1' `
    --add-software-config 'coco_flop:dkong:coco3h -autoboot_delay 2 -autoboot_command RUN\\\"donkey\\\"\n -flop1' `
    --add-software-config 'coco_flop:dkremix:coco3h -autoboot_delay 2 -autoboot_command LOADM\\\"dkremix\\\":exec\n -flop1' `
    --add-software-config 'coco_flop:joust:coco3h -autoboot_delay 2 -autoboot_command RUN\\\"joust\\\"\n -flop1' `
    --add-software-config 'coco_flop:pacman:coco3h -autoboot_delay 2 -autoboot_command RUN\\\"pacman\\\"\n -flop1' `
    --add-software-config 'coco_flop:pitfall2:coco3h -autoboot_delay 2 -autoboot_command RUN\\\"pitfall2\\\"\n -flop1' `
    coco3h

# ----------------------
# Tangerine Oric-1
# ----------------------
python .\src\mess_curator.py search `
    --platform-key tangerine-oric-1 `
    --platform-name-full "Tangerine Oric-1" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput oric1 -autoboot_delay 4 -autoboot_command cload\\\"\\\"\n -cass' `
    --output-format yaml `
    oric1

# ----------------------
# Technosys Aamber Pegasus
# ----------------------
python .\src\mess_curator.py search `
    --platform-key technosys-aamber-pegasus `
    --platform-name-full "Technosys Aamber Pegasus" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput pegasus -rom1" `
    --output-format yaml `
    --add-softlist-config 'pegasus_cart:pegasus -rom1' `
    pegasus

# ----------------------
# Thomson MO6
# ----------------------
python .\src\mess_curator.py search `
    --platform-key thomson-mo6 `
    --platform-name-full "Thomson MO6" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput mo6 -rom1" `
    --output-format yaml `
    --exclude-softlist "mo5_flop mo5_qd mo6_flop" `
    --add-softlist-config 'mo5_cart:mo6 -cart' `
    --add-softlist-config 'mo5_cass:mo6 -cass' `
    --add-softlist-config 'mo6_cass:mo6 -cass' `
    mo6

# ----------------------
# Tiger Electronics Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key tiger-electronics-handhelds-lcd `
    --platform-name-full "Tiger Electronics Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "copycat copycata ditto dxfootb fingbowl hccbaskb rockpin rzbatfor rzindy500 rztoshden subwars t7in1ss taddams taltbeast tapollo13 tbatfor tbatman tbatmana tbtoads tbttf tddragon tddragon2 tddragon3 tdennis tdummies tflash tgaiden tgaiden3 tgargnf tgaunt tgoldeye tgoldnaxe thalone thalone2 thook tinday tjdredd tjpark tkarnov tkazaam tkkongq tlluke2 tmchammer tmegaman3 tmigmax tmkombat tnmarebc topaliens tpitfight trobhood trobocop2 trobocop3 trockteer tsddragon tsf2010 tsfight2 tshadow tsharr2 tsimquest tsjam tskelwarr tsonic tsonic2 tspidman tstrider tsuperman tswampt ttransf2 tvindictr twworld txmen txmenpx"

# ----------------------
# Tiger Game.com
# ----------------------
python .\src\mess_curator.py search `
    --platform-key tiger-game-com `
    --platform-name-full "Tiger Game.com" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gamecom -cart1" `
    --output-format yaml `
    gamecom

# ----------------------
# TimeTop GameKing
# ----------------------
python .\src\mess_curator.py search `
    --platform-key timetop-game-king `
    --platform-name-full "TimeTop GameKing" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gameking -cart" `
    --output-format yaml `
    --exclude-softlist "gameking3" `
    gameking

# ----------------------
# TimeTop GameKing 3
# ----------------------
python .\src\mess_curator.py search `
    --platform-key timetop-game-king-3 `
    --platform-name-full "TimeTop GameKing 3" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gamekin3 -cart" `
    --output-format yaml `
    --exclude-softlist "gameking" `
    gamekin3

# ----------------------
# Tomy evio
# ----------------------
python .\src\mess_curator.py search `
    --platform-key tomy-evio `
    --platform-name-full "Tomy evio" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput evio -cart" `
    --output-format yaml `
    evio

# ----------------------
# Tomy Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key tomy-handhelds-lcd `
    --platform-name-full "Tomy Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "alnchase bombman kingman phpball tbreakup tcaveman tccombat tmbaskb tmpacman tmscramb tmtennis tmtron tmvolleyb"

# ----------------------
# Tomy Tutor
# ----------------------
python .\src\mess_curator.py search `
    --platform-key tomy-tutor `
    --platform-name-full "Tomy Tutor" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput tutor -cart" `
    --output-format yaml `
    --add-softlist-config 'tutor:tutor -cart' `
    tutor

# ----------------------
# Tronica Handhelds (LCD)
# ----------------------
python .\src\mess_curator.py search `
    --platform-key tronica-handhelds-lcd `
    --platform-name-full "Tronica Handhelds (LCD)" `
    --platform-category "Handhelds" "MESS (Handhelds LCD)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "tigarden trclchick trdivadv trsgkeep trshutvoy trspacadv trspacmis trspider trsrescue trthuball"

# ----------------------
# Ultimate Products TV Games
# ----------------------
python .\src\mess_curator.py search `
    --platform-key ultimate-products-tv-games `
    --platform-name-full "Ultimate Products TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "zone100 zone60 zon32bit rockstar react zone40 zonemini"

# ----------------------
# Uzebox
# ----------------------
python .\src\mess_curator.py search `
    --platform-key uzebox `
    --platform-name-full "Uzebox" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput uzebox -cart" `
    --output-format yaml `
    uzebox

# ----------------------
# Vector-06C
# ----------------------
python .\src\mess_curator.py search `
    --platform-key vector-06c `
    --platform-name-full "Vector-06C" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput vector06 -flop1' `
    --output-format yaml `
    --exclude-softlist "vector06_cart" `
    --add-softlist-config 'vector06_flop:vector06 -flop1' `
    vector06

# ----------------------
# VideoBrain Family Computer
# ----------------------
python .\src\mess_curator.py search `
    --platform-key videobrain-family-computer `
    --platform-name-full "VideoBrain Family Computer" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vidbrain -cart1" `
    --output-format yaml `
    --add-softlist-config 'vidbrain:vidbrain -cart1' `
    vidbrain

# ----------------------
# Videoton TVC 64
# ----------------------
python .\src\mess_curator.py search `
    --platform-key videoton-tvc-64 `
    --platform-name-full "Videoton TVC 64" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput tvc64p -cart1" `
    --output-format yaml `
    --exclude-softlist "tvc_flop" `
    --add-softlist-config 'tvc_cart:tvc64p -cart1' `
    --add-softlist-config 'tvc_cass:tvc64p -autoboot_delay 10 -autoboot_command \nLOAD\n -cass1' `
    tvc64p

# ----------------------
# Video Technology Laser 700
# ----------------------
python .\src\mess_curator.py search `
    --platform-key video-technology-laser-700 `
    --platform-name-full "Video Technology Laser 700" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cassette `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput laser700 -cass" `
    --output-format yaml `
    --add-softlist-config 'vtech2_cass:laser700 -autoboot_delay 10 -cass' `
    laser700

# ----------------------
# VTech Creativision
# ----------------------
python .\src\mess_curator.py search `
    --platform-key vtech-creativision `
    --platform-name-full "VTech Creativision" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput crvision -cart" `
    --output-format yaml `
    crvision

# ----------------------
# VTech Genius Leader Color
# ----------------------
python .\src\mess_curator.py search `
    --platform-key vtech-genius-leader-color `
    --platform-name-full "VTech Genius Leader Color" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput glcolor -cart1" `
    --output-format yaml `
    --exclude-softlist "snotec" `
    --add-softlist-config 'glcolor:glcolor -cart1' `
    glcolor

# ----------------------
# VTech Socrates
# ----------------------
python .\src\mess_curator.py search `
    --platform-key vtech-socrates `
    --platform-name-full "VTech Socrates" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput socrates -cart" `
    --output-format yaml `
    socrates

# ----------------------
# VTech TV Games
# ----------------------
python .\src\mess_curator.py search `
    --platform-key vtech-tv-games `
    --platform-name-full "VTech TV Games" `
    --platform-category "Consoles" "MESS (TV Games)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --include-systems "doraglob doraglobf doraglobg doraphon doraphonf hippofr kidizmb kidizmp vtechtvsgr vtechtvssp"

# ----------------------
# VTech VSmile
# ----------------------
python .\src\mess_curator.py search `
    --platform-key vtech-vsmile `
    --platform-name-full "VTech VSmile" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vsmile -cart" `
    --output-format yaml `
    --exclude-softlist "vsmilem_cart" `
    vsmile

# ----------------------
# VTech VSmile Baby
# ----------------------
python .\src\mess_curator.py search `
    --platform-key vtech-vsmile-baby `
    --platform-name-full "VTech VSmile Baby" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vsmileb -cart" `
    --output-format yaml `
    vsmileb

# ----------------------
# VTech VSmile Motion
# ----------------------
python .\src\mess_curator.py search `
    --platform-key vtech-vsmile-motion `
    --platform-name-full "VTech VSmile Motion" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput vsmilem -cart" `
    --output-format yaml `
    --exclude-softlist "vsmile_cart" `
    vsmilem

# ----------------------
# Watara Supervision
# ----------------------
python .\src\mess_curator.py search `
    --platform-key watara-supervision `
    --platform-name-full "Watara Supervision" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput svision -cart" `
    --output-format yaml `
    svision