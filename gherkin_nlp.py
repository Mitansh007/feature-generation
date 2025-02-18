class GherkinGenerator:
    def generate_gherkin(self, elements):
        """Generate Gherkin steps based on UI elements."""
        feature = "Feature: UI Testing\n\nScenario: Detect UI Elements\n"
        
        for element in elements:
            if element["type"] == "button":
                feature += f'  When the user clicks a button at position {element["position"]}\n'
            elif element["type"] == "input_field":
                feature += f'  When the user enters text in the input field at position {element["position"]}\n'
        
        return feature
