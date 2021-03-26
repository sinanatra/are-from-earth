window.addEventListener('DOMContentLoaded', function () {
  /**
  * Fetch analysis results from API.
  *
  * @param {string} text Text to be analyzed.
  * @returns {Promise<prray>} Array of analysis results.
  */
  var fetchFromApi = function (text) {
    var body = new FormData();
    body.append('text', text);

    return fetch('/analyze', { method: 'POST', body: body })
    .then(function (res) {
      return res.json();
    });
  };

  var getSimilarWordsFromApi = function (word, heOrShe) {
    var body = new FormData();
    body.append('word', word);
    body.append('heOrShe', heOrShe);

    return fetch('/similar', { method: 'POST', body: body })
    .then(function (res) {
      return res.json();
    });
  };

  var saveToRemote = function (text) {
    var body = new FormData();
    body.append('text', text);

    return fetch('/upload', { method: 'POST', body: body })
    .then(function (res) {
      return res.json();
    });
  };

  /**
   * Prepare output by highlighting relevant words.
   * @param {string} text Original text.
   * @param {{ [className: string]: string[] }} data Map of CSS classes to lists of relevant words.
   * @return {string}
   *
   */

  var prepareOutput = function (text, data) {
    for (var className in data) {
      for (var i = 0; i < data[className].length; i++) {
        data[className][i] = data[className][i].toLocaleLowerCase();
      }
    }

    text = text.replace(/\b\w+\b/ig, function (word) {
      var lcWord = word.toLocaleLowerCase();
      for (var className in data) {
        if (data[className].indexOf(lcWord) !== -1) {
          return '<mark id="' + className + '">' + word + '</mark>';
        }
      }

      return word;
    });

    return text;
  };


  var input = document.getElementById('input');
  var output = document.getElementById('output'); 
  var shescore = document.getElementById('shescore'); 
  var hescore = document.getElementById('hescore'); 
  var parseBtn = document.getElementById('parse');
  var uploadBtn = document.getElementById('upload');

  uploadBtn.addEventListener('click', function (event) {
    event.preventDefault();
    event.stopPropagation();

    var text = input.innerText;
    saveToRemote(text);
  });



  parseBtn.addEventListener('click', function (evt) {
    evt.preventDefault();
    evt.stopPropagation();

    parseBtn.setAttribute('disabled', true);

    var text = input.innerText;
    fetchFromApi(text)
    .then(function (analysis) {
      var she_analysis = analysis[0];
      var he_analysis = analysis[1];
      var sheScores = analysis[2];
      var heScores = analysis[3];

      var outputHTML = prepareOutput(text, {
        'she123': she_analysis,
        'he123': he_analysis,
      });

      outputHTML = outputHTML.trim().split(/[\r\n]{2,}/g)
      .map(function (para) {
        return '<p>' + para + '</p>';
      })
      .join('\n');

      var processed = [];

      output.innerHTML = outputHTML;
      sheScores = sheScores
      .filter(function (a) {
        if (processed.indexOf(a[0]) === -1) {
          processed.push(a[0]);
          return true;
        }
        return false;
      })
      .sort(function (a, b) {
        return b[1] - a[1] ;
      })
      .map(function (a) {
        var opacity = Math.max(Math.min((a[1] - 30) * 2, 100),2);
        return '<p>' + a[0]+ '</p>  <h3>'  + a[1] + '% Female</h3>';
      })
      .join('<br>');

      var female = document.getElementById('she123'); 
      var male = document.getElementById('he123'); 
    

      shescore.innerHTML = sheScores;
      output.querySelectorAll('#she123')
        .forEach(function (a) {
          a.addEventListener('click', function (event) {
            event.preventDefault();
            var word = a.innerText;
            
          });
        });

      processed = [];

      heScores = heScores
      .filter(function (a) {
        if (processed.indexOf(a[0]) === -1) {
          processed.push(a[0]);
          return true;
        }
        return false;
      })
      .sort(function (a, b) {
        return  b[1] - a[1];
      })
      .map(function (a) {
        var opacity = Math.max(Math.min((a[1] - 30) * 2, 100),2);
        return '<p >' + a[0]+ '</p>  <h3>'  + a[1] + '% Male</h3>';
      })
      .join('<br>');

      hescore.innerHTML = heScores;
      output.querySelectorAll('#he123')
        .forEach(function (a) {
          a.addEventListener('click', function (event) {
            event.preventDefault();
            var word = a.innerText;
            
          });
        });


      parseBtn.removeAttribute('disabled');

      console.debug('Analyzed text:', text);
      console.debug('Analysis results:', analysis);
    })
    .catch(function (error) {
      output.innerHTML = '';
      parseBtn.removeAttribute('disabled');

      window.alert('Sorry, an error occurred!');
      console.error('Error!', error);
    });
  });
});
