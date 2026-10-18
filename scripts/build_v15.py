"""V1.5: room 2 for 12 guests, two squat stalls per WC, male urinals at top."""
from build_v13 import Revision, main

if __name__ == '__main__':
    main(Revision(
        version='V1.5',
        room_two_length=4000,
        bottom_squats=True,
        screen_face_y=10000,
        row_extra_clearance=50,
        room_two_diameter=1800,
        room_two_seats=12,
        room_two_center_x=12415,
        two_squats=True,
        male_urinals_top=True,
        male_wc_door=True,
    ))
