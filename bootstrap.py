"""
Lavalink on Heroku bootstrap script
Credit to diniboy for sed script
"""

from os import system, environ


class LavalinkBootstrap:

    """
    Class we're using to get Lavalink working on Heroku
    """

    def __init__(self):

        """
        Doing important stuff here
        """
        self._lavalink_version = "3.2.2" if not environ.get('LAVALINK_VERSION') else environ.get('LAVALINK_VERSION')

        self.download_command = "wget https://github.com/Frederikam/Lavalink/releases/download/{self._lavalink_version}/Lavalink.jar"

        self.replace_port_command = 'sed -i "s|DYNAMICPORT|$PORT|" application.yml'

        self.replace_password_command = 'sed -i "s|DYNAMICPASSWORD|$PASSWORD|" application.yml'
        self.replace_password_command_no_password = 'sed -i "s|DYNAMICPASSWORD|youshallnotpass|" application.yml'
        
        self._additional_options = environ.get(
            "ADDITIONAL_JAVA_OPTIONS"
        ) # Heroku provides basic Java configuration based on dyno size, no need in limiting memory
    
        self.run_command = f"java -jar Lavalink.jar {self._additional_options}" # User-provided config, will override heroku's

    def replace_password_and_port(self):

        """
        Replacing password and port in application.yml
        """

        print(
            "[INFO] Replacing port..."
        )

        try:
            
            system(
                self.replace_port_command
            )

            if not environ.get("PASSWORD"):

                print(
                    """
                    [WARNING] You have not specified your Lavalink password in config vars. To do this, go to settings 
                    and set the PASSWORD environment variable
                    """
                )
    
                return system(
                    self.replace_password_command_no_password
                )
            
            system(
                self.replace_password_command
            )

        except BaseException as exc:

            print(
                f"[ERROR] Failed to replace port/password. Info: {exc}"
            )

        else:

            print(
                "[INFO] Done. Config is ready now"
            )

    def download(self):

        """
        Downloads latest release of Lavalink
        """

        print(
            "[INFO] Downloading latest release of Lavalink..."
        )
        
        try:
            
            system(
                self.download_command
            )
        
        except BaseException as exc:

            print(
                f"[ERROR] Lavalink download failed. Info: {exc}"
            )

        else:
        
            print(
                "[INFO] Lavalink download OK"
            )
    
    def run(self):

        """
        Runs Lavalink instance
        """

        self.download()
        self.replace_password_and_port()

        print(
            "[INFO] Starting Lavalink..."
        )

        try:

            system(
                self.run_command
            )
        
        except BaseException as exc:

            print(
                f"[ERROR] Failed to start Lavalink. Info: {exc}"
            )

if __name__ == "__main__":

    """
    Starts our instance
    """

    LavalinkBootstrap().run()