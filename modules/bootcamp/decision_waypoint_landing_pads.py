"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""
# Disable for bootcamp use
# pylint: disable=unused-import


from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# pylint: disable=unused-argument,line-too-long


# All logic around the run() method
# pylint: disable-next=too-few-public-methods
class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """
    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.waypoint_found = False
        self.landing_pad_found = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        if report.status == drone_status.DroneStatus.HALTED and not self.waypoint_found:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, 
                self.waypoint.location_y
            )
            self.waypoint_found = True

        elif report.status == drone_status.DroneStatus.HALTED and not self.landing_pad_found:
            min_distance = float('inf')
            closest_pad = None
            
            for pad in landing_pad_locations:
                distance = self.distance(report.position, pad)
                if distance < min_distance:
                    min_distance = distance
                    closest_pad = pad
            
            if closest_pad is not None:
                command = commands.Command.create_set_relative_destination_command(
                    closest_pad.location_x - report.position.location_x,
                    closest_pad.location_y - report.position.location_y
                )
                self.landing_pad_found = True

        elif report.status == drone_status.DroneStatus.HALTED and self.landing_pad_found:
            command = commands.Command.create_land_command()
            
        return command

    def distance(self, l1: location.Location, l2: location.Location):
        return (l1.location_x - l2.location_x)**2 + (l1.location_y - l2.location_y)**2
    