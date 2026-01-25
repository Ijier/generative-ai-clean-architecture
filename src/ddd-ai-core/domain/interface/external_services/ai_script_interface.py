from abc import ABC, abstractmethod


class AiScriptInterface(ABC):
    @abstractmethod
    def generate_script(self, domain1: domain1, domain2: domain2) -> domain3:
        """Generate domain1 domain3

        Args:
            domain1 (domain1): The domain1 to generate a domain3 for
            domain2 (domain2): The domain2 settings (domain2 domain model)

        Returns:
            domain3: The generated domain3
        """
        pass

    @abstractmethod
    def parse_script_to_ssml(self, domain3: domain3, domain2: domain2) -> domain4:
        """Parse a domain3 into some format.
        Args:
            domain3 (domain3): The generated domain3 data
            domain2 (domain2): The domain2 settings (domain2 domain model)
        """
        pass
