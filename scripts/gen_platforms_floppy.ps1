# ----------------------
# Acorn Archimedes
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key acorn-archimedes `
    --platform-name-full "Acorn Archimedes" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Computers)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput aa4401 -flop' `
    --output-format yaml `
    --output-file system_softlist.yml `
    aa4401

# ----------------------
# Acorn Atom
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key acorn-atom `
    --platform-name-full "Acorn Atom" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Computers)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput atom -autoboot_delay \"2\" -autoboot_command \"DOS\nCAT\n*RUN\"\" -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    atom

# ----------------------
# Amstrad CPC
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key amstrad-cpc `
    --platform-name-full "Amstrad CPC" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Computers)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput cpc6128 -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    cpc6128

# ----------------------
# BBC Microcomputer System
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key bbc-microcomputer-system `
    --platform-name-full "BBC Microcomputer System" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Computers)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput bbcb -skip_gameinfo -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    bbcb

# ----------------------
# Camputers Lynx
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key camputers-lynx `
    --platform-name-full "Camputers Lynx" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Computers)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput lynx128k -autoboot_delay \"2\" -autoboot_command \"XROM\n\n\nEXT DIR\n\n\n\n\n\n\n\nEXT LOAD \"\" -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    lynx128k 
    
# ----------------------
# Coleco ADAM
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key coleco-adam `
    --platform-name-full "Coleco ADAM" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Computers)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput adam -skip_gameinfo -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    adam
    
# ----------------------
# SAM Coupe
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key sam-coupe `
    --platform-name-full "SAM Coupe" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Computers)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput samcoupe -autoboot_delay 2 -skip_gameinfo -autoboot_command \"\nBOOT\n\" -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    samcoupe  
    
# ----------------------
# Sharp MZ-2500
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key sharp-mz-2500 `
    --platform-name-full "Sharp MZ-2500" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Computers)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput mz2500 -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    mz2500   
    
# ----------------------
# Vector-06C
# ----------------------
python ..\src\mess_curator.py search by-name `
    --platform-key vector-06c `
    --platform-name-full "Vector-06C" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type floppy `
    --emu-name "MAME (Computers)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput vector06 -flop1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    vector06    