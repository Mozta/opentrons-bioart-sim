from opentrons import types

import string

metadata = {
    'protocolName': '{YOUR NAME} - Opentrons Art - HTGAA',
    'author': 'HTGAA',
    'source': 'HTGAA 2026',
    'apiLevel': '2.20'
}

Z_VALUE_AGAR = 2.0
POINT_SIZE = 1

mrfp1_points = [(0,14), (2,14), (4,14), (0,12), (0,10), (6,10), (0,8), (6,8), (0,6), (6,6), (6,4), (-10,-4), (-4,-4), (-10,-6), (-4,-6), (-10,-8), (-4,-8), (-10,-10), (-4,-10), (-10,-12), (-4,-12), (-6,-14)]
mscarlet_i_points = [(0,16), (2,16), (4,16), (-2,14), (-2,12), (-2,10), (2,10), (4,10), (-2,8), (4,8), (-2,6), (4,6), (0,4), (2,4), (4,4), (-10,-2), (-8,-2), (-6,-2), (-12,-4), (-6,-4), (-12,-6), (-6,-6), (-12,-8), (-6,-8), (-12,-10), (-6,-10), (-12,-12), (-6,-12), (-10,-14), (-8,-14)]
mcerulean3_points = [(-6,16), (-16,14), (-14,14), (-10,14), (-8,14), (-6,14), (-10,12), (-10,10), (-10,8), (-10,6), (-10,4), (-18,-4), (10,-4), (-18,-6), (10,-6), (-18,-8), (10,-8), (-24,-14), (-22,-14), (-20,-14), (-18,-14), (4,-14), (6,-14), (8,-14), (10,-14)]
mjuniper_points = [(-16,16), (-14,16), (-12,16), (-10,16), (-8,16), (-12,14), (-12,12), (-12,10), (-12,8), (-12,6), (-12,4)]
mclover3_points = [(-28,16), (-22,16), (-28,14), (-22,14), (-28,12), (-22,12), (-26,10), (-24,10), (-28,8), (-22,8), (-28,6), (-22,6), (-28,4), (-22,4), (-22,-2), (-20,-2), (6,-2), (8,-2), (-20,-4), (8,-4), (-20,-6), (8,-6), (-20,-8), (8,-8), (-22,-10), (6,-10), (4,-12), (2,-14)]
avgfp_points = [(-26,16), (-20,16), (-26,14), (-20,14), (-26,12), (-20,12), (-22,10), (-26,8), (-20,8), (-26,6), (-20,6), (-26,4), (-20,4)]
mpapaya_points = [(-24,-2), (4,-2), (-26,-4), (2,-4), (-24,-12), (-26,-14)]
azurite_points = [(12,16), (14,16), (16,16), (24,16), (26,16), (28,16), (10,14), (16,14), (22,14), (28,14), (10,12), (16,12), (22,12), (28,12), (10,10), (16,10), (22,10), (28,10), (10,8), (16,8), (22,8), (28,8), (10,6), (16,6), (22,6), (28,6), (10,4), (16,4), (22,4), (28,4), (18,-2), (20,-2), (22,-2), (16,-4), (16,-6), (16,-8), (18,-8), (20,-8), (22,-8), (16,-10), (22,-10), (16,-12), (22,-12), (18,-14), (20,-14)]
electra2_points = [(12,14), (18,14), (24,14), (30,14), (12,12), (18,12), (24,12), (30,12), (12,10), (14,10), (18,10), (24,10), (26,10), (30,10), (12,8), (18,8), (24,8), (30,8), (12,6), (18,6), (24,6), (30,6), (12,4), (18,4), (24,4), (30,4), (18,-4), (18,-6), (24,-8), (18,-10), (24,-10), (18,-12), (24,-12), (22,-14)]

point_name_pairing = [("mrfp1", mrfp1_points),("mscarlet_i", mscarlet_i_points),("mcerulean3", mcerulean3_points),("mjuniper", mjuniper_points),("mclover3", mclover3_points),("avgfp", avgfp_points),("mpapaya", mpapaya_points),("azurite", azurite_points),("electra2", electra2_points)]

# Robot deck setup constants
TIP_RACK_DECK_SLOT = 9
COLORS_DECK_SLOT = 6
AGAR_DECK_SLOT = 5
PIPETTE_STARTING_TIP_WELL = 'A1'

# Place the PCR tubes in this order
well_colors = {
    'A1': 'sfGFP',
    'A2': 'mRFP1',
    'A3': 'mKO2',
    'A4': 'Venus',
    'A5': 'mKate2_TF',
    'A6': 'Azurite',
    'A7': 'mCerulean3',
    'A8': 'mClover3',
    'A9': 'mJuniper',
    'A10': 'mTurquoise2',
    'A11': 'mBanana',
    'A12': 'mPlum',
    'B1': 'Electra2',
    'B2': 'mWasabi',
    'B3': 'mScarlet_I',
    'B4': 'mPapaya',
    'B5': 'eqFP578',
    'B6': 'tdTomato',
    'B7': 'DsRed',
    'B8': 'mKate2',
    'B9': 'EGFP',
    'B10': 'mRuby2',
    'B11': 'TagBFP',
    'B12': 'mChartreuse_TF',
    'C1': 'mLychee_TF',
    'C2': 'mTagBFP2',
    'C3': 'mEGFP',
    'C4': 'mNeonGreen',
    'C5': 'mAzamiGreen',
    'C6': 'mWatermelon',
    'C7': 'avGFP',
    'C8': 'mCitrine',
    'C9': 'mVenus',
    'C10': 'mCherry',
    'C11': 'mHoneydew',
    'C12': 'TagRFP',
    'D1': 'mTFP1',
    'D2': 'Ultramarine',
    'D3': 'ZsGreen1',
    'D4': 'mMiCy',
    'D5': 'mStayGold2',
    'D6': 'PA_GFP'
}

volume_used = {
    'mrfp1': 0,
    'mscarlet_i': 0,
    'mcerulean3': 0,
    'mjuniper': 0,
    'mclover3': 0,
    'avgfp': 0,
    'mpapaya': 0,
    'azurite': 0,
    'electra2': 0
}

def update_volume_remaining(current_color, quantity_to_aspirate):
    rows = string.ascii_uppercase
    for well, color in list(well_colors.items()):
        if color == current_color:
            if (volume_used[current_color] + quantity_to_aspirate) > 250:
                # Move to next well horizontally by advancing row letter, keeping column number
                row = well[0]
                col = well[1:]
                
                # Find next row letter
                next_row = rows[rows.index(row) + 1]
                next_well = f"{next_row}{col}"
                
                del well_colors[well]
                well_colors[next_well] = current_color
                volume_used[current_color] = quantity_to_aspirate
            else:
                volume_used[current_color] += quantity_to_aspirate
            break

def run(protocol):
    # Load labware, modules and pipettes
    protocol.home()

    # Tips
    tips_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', TIP_RACK_DECK_SLOT, 'Opentrons 20uL Tips')

    # Pipettes
    pipette_20ul = protocol.load_instrument("p20_single_gen2", "right", [tips_20ul])

    # Deep Well Plate
    temperature_plate = protocol.load_labware('nest_96_wellplate_2ml_deep', 6)

    # Agar Plate
    agar_plate = protocol.load_labware('htgaa_agar_plate', AGAR_DECK_SLOT, 'Agar Plate')
    agar_plate.set_offset(x=0.00, y=0.00, z=Z_VALUE_AGAR)

    # Get the top-center of the plate, make sure the plate was calibrated before running this
    center_location = agar_plate['A1'].top()

    pipette_20ul.starting_tip = tips_20ul.well(PIPETTE_STARTING_TIP_WELL)
    
    # Helper function (dispensing)
    def dispense_and_jog(pipette, volume, location):
        assert(isinstance(volume, (int, float)))
        # Go above the location
        above_location = location.move(types.Point(z=location.point.z + 2))
        pipette.move_to(above_location)
        # Go downwards and dispense
        pipette.dispense(volume, location)
        # Go upwards to avoid smearing
        pipette.move_to(above_location)

    # Helper function (color location)
    def location_of_color(color_string):
        for well,color in well_colors.items():
            if color.lower() == color_string.lower():
                return temperature_plate[well]
        raise ValueError(f"No well found with color {color_string}")

    # Print pattern by iterating over lists
    for i, (current_color, point_list) in enumerate(point_name_pairing):
        # Skip the rest of the loop if the list is empty
        if not point_list:
            continue

        # Get the tip for this run, set the bacteria color, and the aspirate bacteria of choice
        pipette_20ul.pick_up_tip()
        max_aspirate = int(18 // POINT_SIZE) * POINT_SIZE
        quantity_to_aspirate = min(len(point_list)*POINT_SIZE, max_aspirate)
        update_volume_remaining(current_color, quantity_to_aspirate)
        pipette_20ul.aspirate(quantity_to_aspirate, location_of_color(current_color))

        # Iterate over the current points list and dispense them, refilling along the way
        for i in range(len(point_list)):
            x, y = point_list[i]
            adjusted_location = center_location.move(types.Point(x, y))

            dispense_and_jog(pipette_20ul, POINT_SIZE, adjusted_location)
            
            if pipette_20ul.current_volume == 0 and len(point_list[i+1:]) > 0:
                quantity_to_aspirate = min(len(point_list[i:])*POINT_SIZE, max_aspirate)
                update_volume_remaining(current_color, quantity_to_aspirate)
                pipette_20ul.aspirate(quantity_to_aspirate, location_of_color(current_color))

        # Drop tip between each color
        pipette_20ul.drop_tip()
    