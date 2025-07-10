# ----------------------
# Acorn Archimedes (moved)
# ----------------------
python .\src\mess_curator.py search by-name `
    --platform-key acorn-archimedes `
    --platform-name-full "Acorn Archimedes" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Floppy)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput aa4401 -flop' `
    --output-format yaml `
    --output-file system_softlist2.yml `
    aa4401

# ----------------------
# Acorn Atom (Moved to All)
# ----------------------
python .\src\mess_curator.py search by-name `
    --platform-key acorn-atom `
    --platform-name-full "Acorn Atom" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Floppy)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput atom -autoboot_delay \"2\" -autoboot_command \"DOS\nCAT\n*RUN\"\" -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
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
# Amstrad CPC (moved)
# ----------------------
python .\src\mess_curator.py search by-name `
    --platform-key amstrad-cpc `
    --platform-name-full "Amstrad CPC" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Floppy)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput cpc6128 -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    cpc6128

# ----------------------
# BBC Microcomputer System (Moved to All)
# ----------------------
python .\src\mess_curator.py search by-name `
    --platform-key bbc-microcomputer-system `
    --platform-name-full "BBC Microcomputer System" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Floppy)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput bbcb -skip_gameinfo -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    bbcb

# ----------------------
# Camputers Lynx (Moved to All)
# ----------------------
python .\src\mess_curator.py search by-name `
    --platform-key camputers-lynx `
    --platform-name-full "Camputers Lynx" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Floppy)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput lynx128k -autoboot_delay \"2\" -autoboot_command \"XROM\n\n\nEXT DIR\n\n\n\n\n\n\n\nEXT LOAD \"\" -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    lynx128k 
    
# ----------------------
# Coleco ADAM (moved)
# ----------------------
python .\src\mess_curator.py search by-name `
    --platform-key coleco-adam `
    --platform-name-full "Coleco ADAM" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Floppy)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput adam -skip_gameinfo -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    adam
    
# ----------------------
# SAM Coupe (Moved to All)
# ----------------------
python .\src\mess_curator.py search by-name `
    --platform-key sam-coupe `
    --platform-name-full "SAM Coupe" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Floppy)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput samcoupe -autoboot_delay 2 -skip_gameinfo -autoboot_command \"\nBOOT\n\" -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    samcoupe  
    
# ----------------------
# Sharp MZ-2500 (moved)
# ----------------------
python .\src\mess_curator.py search by-name `
    --platform-key sharp-mz-2500 `
    --platform-name-full "Sharp MZ-2500" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Floppy)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput mz2500 -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    mz2500   
    
# ----------------------
# Vector-06C (moved)
# ----------------------
python .\src\mess_curator.py search by-name `
    --platform-key vector-06c `
    --platform-name-full "Vector-06C" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Floppy)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput vector06 -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    vector06    