import math

class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.centerPoints = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.idCount = 1


    def update(self, objectsRect):
        # Objects boxes and ids
        objectsBoxsID = []

        # Get center point of new object
        for rect in objectsRect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            sameObjectDetected = False
            for ID, pt in self.centerPoints.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 25:
                    self.centerPoints[ID] = (cx, cy)
                    print(self.centerPoints)
                    objectsBoxsID.append([x, y, w, h, ID])
                    sameObjectDetected = True
                    break

            # New object is detected we assign the ID to that object
            if sameObjectDetected is False:
                self.centerPoints[self.idCount] = (cx, cy)
                objectsBoxsID.append([x, y, w, h, self.idCount])
                self.idCount += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        newCenterPoints = {}
        for objBoxID in objectsBoxsID:
            _, _, _, _, objectID = objBoxID
            center = self.centerPoints[objectID]
            newCenterPoints[objectID] = center

        # Update dictionary with IDs not used removed
        self.centerPoints = newCenterPoints.copy()
        return objectsBoxsID