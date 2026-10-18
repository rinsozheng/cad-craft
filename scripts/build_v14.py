"""V1.4: enlarge upper private room, shift the dining row, correct WC zones."""
from build_v13 import Revision, main

if __name__ == '__main__':
    main(Revision(
        version='V1.4',
        room_two_length=4000,
        bottom_squats=True,
        screen_face_y=10000,
        row_extra_clearance=50,
    ))
