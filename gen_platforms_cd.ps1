# ----------------------
# Mattel Hyperscan (moved)
# ----------------------
python .\src\mess_curator.py search by-name `
    --platform-key mattel-hyperscan `
    --platform-name-full "Mattel Hyperscan" `
    --platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
    --media-type cdrom `
    --emu-name "MAME (CD)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput hyprscan -cdrom' `
    --output-format yaml `
    --output-file system_softlist.yml `
    --exclude-softlist "hyperscan_card" `
    hyprscan

# ----------------------
# Tandy Memorex VIS (moved)
# ----------------------
python .\src\mess_curator.py search by-name `
--platform-key tandy-memorex-vis `
--platform-name-full "Tandy Memorex VIS" `
--platform-category "Consoles" "MESS (Consoles)" "MESS (System w/ Softlist)" `
--media-type cdrom `
--emu-name "MAME (CD)" `
--default-emu `
--default-emu-cmd-params '-keyboardprovider dinput vis -cdrom' `
--output-format yaml `
--output-file system_softlist.yml `
vis