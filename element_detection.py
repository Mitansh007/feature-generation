import cv2

class ElementDetector:
    def detect_elements(self, image_path):
        """Detect simple rectangular shapes for buttons or fields."""
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Thresholding to binary
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        elements = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if 30 < w < 300 and 30 < h < 300:  # Ignore too small/large elements
                elements.append({
                    "type": "button" if w > h else "input_field",
                    "position": (x, y, w, h)
                })
        return elements
