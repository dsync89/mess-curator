# ----------------------
# Acorn Electron
# ----------------------
python .\mess_curator.py search by-name `
    --platform-key acorn-electron `
    --platform-name-full "Acorn Electron" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cassette)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput electron -skip_gameinfo -autoboot_delay "2" -autoboot_command "*tape\nchain""""""\n" -cass' `
    --output-format yaml `
    --output-file system_softlist.yml `
    electron

# ----------------------
# EACA EG2000 Colour Genie
# ----------------------
python .\mess_curator.py search by-name `
    --platform-key eaca-eg2000-colour-genie `
    --platform-name-full "EACA EG2000 Colour Genie" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cassette)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput cgenie -autoboot_command \n\nCLOAD\n -autoboot_delay 1 -cass' `
    --output-format yaml `
    --output-file system_softlist.yml `
    cgenie

# ----------------------
# Exidy Sorcerer
# ----------------------
python .\mess_curator.py search by-name `
    --platform-key exidy-sorcerer `
    --platform-name-full "Exidy Sorcerer" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cassette)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput sorcerer2 -autoboot_command "LOG\n" -autoboot_delay 3 -cass1' `
    --output-format yaml `
    --output-file system_softlist.yml `
    sorcerer2

# ----------------------
# Memotech MTX
# ----------------------
python .\mess_curator.py search by-name `
    --platform-key memotech-mtx `
    --platform-name-full "Memotech MTX" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cassette)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput mtx512 -skip_gameinfo -autoboot_command "load""""""\n" -autoboot_delay 3 -cass' `
    --output-format yaml `
    --output-file system_softlist.yml `
    mtx512    

# ----------------------
# Philips VG 5000
# ----------------------
python .\mess_curator.py search by-name `
    --platform-key philips-vg-5000 `
    --platform-name-full "Philips VG 5000" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cassette)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput vg5k -skip_gameinfo -autoboot_command "cload\n" -autoboot_delay 3 -cass' `
    --output-format yaml `
    --output-file system_softlist.yml `
    vg5k

# ----------------------
# Tandy TRS-80
# ----------------------
python .\mess_curator.py search by-name `
    --platform-key tandy-trs-80 `
    --platform-name-full "Tandy TRS-80" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cassette)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput trs80 -cass' `
    --output-format yaml `
    --output-file system_softlist.yml `
    trs80
    
# ----------------------
# Tangerine Oric-1
# ----------------------
python .\mess_curator.py search by-name `
    --platform-key tangerine-oric-1 `
    --platform-name-full "Tangerine Oric-1" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cartridge `
    --emu-name "MAME (Cassette)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput oric1 -autoboot_delay 4 -autoboot_command cload\"\"\n -cass' `
    --output-format yaml `
    --output-file system_softlist.yml `
    oric1         