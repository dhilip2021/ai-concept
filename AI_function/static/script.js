<script>
    $(document).ready(function() {
      const form = $('#voiceForm');
      const capturedText = $('#capturedText');
      const startButton = $('#startButton');
      console.log(form);
      console.log(capturedText);
      console.log(startButton);
    
      startButton.on('click', function() {
        const recognition = window.webkitSpeechRecognition || window.SpeechRecognition;
        console.log(recognition);
      
        if (recognition) {
          const recognizer = new recognition();
          console.log(recognizer);
          recognizer.lang = 'en-US';
    
          recognizer.onresult = function(event) {
            const result = event.results[event.results.length - 1][0].transcript;
            console.log(result);
            capturedText.val(result);
            form.submit();
          };
    
          recognizer.start();
        } else {
          console.log('Web Speech API not supported');
          // Display an error message or fallback behavior
        }
      });
    });
  </script>