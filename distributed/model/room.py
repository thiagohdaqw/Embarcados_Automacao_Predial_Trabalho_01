from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RoomGPIO:
	name:				str

	dth22:				int

	alarm:				int
	lamp01:				int
	lamp02:				int
	projector:			int
	air_conditioning:   int

	smoke:				int
	window:				int
	door:				int
	door_in:			int
	door_out:			int
	presence:			int


@dataclass
class Room:
	name:				str

	temperature: 		Optional[float] = field(default=None)
	humidity:			Optional[int]   = field(default=None)

	persons: 			int = field(default=0)
	
	alarm:			  	bool	= field(default=False)
	lamp01:				bool	= field(default=False)
	lamp02:				bool	= field(default=False)
	projector:			bool	= field(default=False)
	air_conditioning:   bool	= field(default=False)
	
	door:				bool	= field(default=False)
	smoke:				bool	= field(default=False)
	window:				bool	= field(default=False)
	presence:			bool	= field(default=False)
