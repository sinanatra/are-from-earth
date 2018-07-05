window.addEventListener('DOMContentLoaded', function () {
  /**
  * Fetch analysis results from API.
  *
  * @param {string} text Text to be analyzed.
  * @returns {Promise<Array>} Array of analysis results.
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
  var output = document.getElementById('output'); // Se l'ID dell'elemento HTML è cambiato, cambia questo.
  var shescore = document.getElementById('shescore'); // Se l'ID dell'elemento HTML è cambiato, cambia questo.
  var hescore = document.getElementById('hescore'); // Se l'ID dell'elemento HTML è cambiato, cambia questo.
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

      // var outputHTML = prepareOutput(text, she_analysis, 'she123');
      // outputHTML = prepareOutput(outputHTML, he_analysis, 'he123');

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
      // Questo sarà sheScores = ['boss', 'guy', 'programmer']
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
        return '<a style="opacity: ' + (opacity / 100)  + '"' + ' onMouseOver=' + '"this.style.opacity='+ '1"'+ ' onMouseOut=' + '"this.style.opacity=' + opacity/100 + ';" href="#">' + a[0]+ '</a> <!-- <h3>'  + a[1] + '%</h3> -->';
      })
      .join('<br>');

      var female = document.getElementById('she123'); // Se l'ID dell'elemento HTML è cambiato, cambia questo.
      var male = document.getElementById('he123'); // Se l'ID dell'elemento HTML è cambiato, cambia questo.
    

      shescore.innerHTML = sheScores;
      output.querySelectorAll('#she123')
        .forEach(function (a) {
          a.addEventListener('click', function (event) {
            event.preventDefault();
            var word = a.innerText;
            getSimilarWordsFromApi(word, "she")
            .then(function (res) {
              var associations= document.getElementById('associations');
                associations.innerHTML = res
                   .map(function (tuple) {
                    var opacity = Math.max(Math.min((tuple[1] - 30) * 2, 100),0.2);
                    return '<span class="female" style="opacity: ' + tuple[1] +'"' + ' onMouseOver=' + '"this.style.opacity='+ '1"'+ ' onMouseOut=' + '"this.style.opacity=' + tuple[1] +  ';" href="#">' + tuple[0] + '</span>';
                  })
                  .join('<br>');
                associations.querySelectorAll('span')
                  .forEach(function (a) {
                    a.addEventListener('click', function (event) {
                      event.preventDefault();
                      var word = a.innerText;
                      getSimilarWordsFromApi(word, "she")
                      .then(function (res) {
                          document.getElementById('second_associations').innerHTML = res
                            .map(function (tuple) {
                              var opacity = Math.max(Math.min((tuple[1] - 30) * 2, 100),0.2);
                              return '<span class="female" style="opacity: ' + tuple[1] +'"' + ' onMouseOver=' + '"this.style.opacity='+ '1"'+ ' onMouseOut=' + '"this.style.opacity=' + tuple[1] +  ';" href="#">'+ tuple[0] + '</span>';
                            })
                            .join('<br>');
                            second_associations.querySelectorAll('span')
                              .forEach(function (a) {
                                a.addEventListener('click', function (event) {
                                  event.preventDefault();
                                  var word = a.innerText;
                                  getSimilarWordsFromApi(word, "she")
                                  .then(function (res) {
                                      document.getElementById('third_associations').innerHTML = res
                                        .map(function (tuple) {
                                          var opacity = Math.max(Math.min((tuple[1] - 30) * 2, 100),0.2);
                                          return '<span class="female" style="opacity: ' + tuple[1] +'"' + ' onMouseOver=' + '"this.style.opacity='+ '1"'+ ' onMouseOut=' + '"this.style.opacity=' + tuple[1] +  ';" href="#">' + tuple[0] + '</span>';
                                        })
                                        .join('<br>');
                                    });
                                });
                              });
                        });
                    });
                  });
              });
          });
        });

      processed = [];

      // Questo sarà heScores = ['guy', 'boss', 'programmer']
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
        return '<a style="opacity: ' + (opacity / 100) + '"' + ' onMouseOver=' + '"this.style.opacity='+ '1"'+ ' onMouseOut=' + '"this.style.opacity=' + opacity/100 + ';" href="#">' + a[0]+ '</a> <!-- <h3>'  + a[1] + '%</h3> -->';
      })
      .join('<br>');

      hescore.innerHTML = heScores;
      output.querySelectorAll('#he123')
        .forEach(function (a) {
          a.addEventListener('click', function (event) {
            event.preventDefault();
            var word = a.innerText;
            getSimilarWordsFromApi(word, "he")
            .then(function (res) {
                var associations= document.getElementById('associations');
                associations.innerHTML = res
                  .map(function (tuple) {
                    var opacity = Math.max(Math.min((tuple[1] - 30) * 2, 100),0.2);
                    return '<span class="male" style="opacity: ' + tuple[1] +'"' + ' onMouseOver=' + '"this.style.opacity='+ '1"'+ ' onMouseOut=' + '"this.style.opacity=' + tuple[1] +  ';" href="#">' + tuple[0] + '</span>';
                  })
                  .join('<br>');
                associations.querySelectorAll('span')
                  .forEach(function (a) {
                    a.addEventListener('click', function (event) {
                      event.preventDefault();
                      var word = a.innerText;
                      getSimilarWordsFromApi(word, "he")
                      .then(function (res) {
                        var second_associations = document.getElementById('second_associations');
                         second_associations.innerHTML = res
                            .map(function (tuple) {
                              var opacity = Math.max(Math.min((tuple[1] - 30) * 2, 100),0.2);
                              return '<span class="male" style="opacity: ' + tuple[1] +'"' + ' onMouseOver=' + '"this.style.opacity='+ '1"'+ ' onMouseOut=' + '"this.style.opacity=' + tuple[1] +  ';" href="#">' + tuple[0] + '</span>';
                            })
                            .join('<br>');
                            second_associations.querySelectorAll('span')
                              .forEach(function (a) {
                                a.addEventListener('click', function (event) {
                                  event.preventDefault();
                                  var word = a.innerText;
                                  getSimilarWordsFromApi(word, "he")
                                  .then(function (res) {
                                      document.getElementById('third_associations').innerHTML = res
                                        .map(function (tuple) {
                                          var opacity = Math.max(Math.min((tuple[1] - 30) * 2, 100),0.2);
                                          return '<span class="male" style="opacity: ' + tuple[1] +'"' + ' onMouseOver=' + '"this.style.opacity='+ '1"'+ ' onMouseOut=' + '"this.style.opacity=' + tuple[1] +  ';" href="#">' + tuple[0] + '</span>';
                                        })
                                        .join('<br>');
                                    });
                                });
                              });
                        });
                    });
                  });
              });
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
