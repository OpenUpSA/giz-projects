jQuery.support.cors = true;

// attach browser dimensions for help with charts and tables
window.browserWidth = document.documentElement.clientWidth;
window.browserHeight = document.documentElement.clientHeight;

$(document).ready(function(){
  // prepare ajax spinners
  $('body').append('<div id="body-spinner"></div>');
  var spinnerTarget = document.getElementById('body-spinner'),
      spinner = new Spinner();

  if ($('#profile').length > 0) {
    // profile page stuff

    //Get page-nav offset from top of page
    var pagenavOffset = $('.page-nav-container').offset().top;

    //Affix page-nav to top of page on scroll
    $('.page-nav-container').affix({
      offset: {
        top: pagenavOffset
      }
    });

    //Expand page-nav once affixed
    $('.page-nav-container').on('affixed.bs.affix', function () {
      $('.page-nav-wrapper').addClass('expanded');
    });

    //Un-expand page-nav once nolonger affixed
    $('.page-nav-container').on('affixed-top.bs.affix', function () {
      $('.page-nav-wrapper').removeClass('expanded');
    });

    //Change active tab when scrolling using Bootstrap scrollspy.js
    $('body').scrollspy({
      target: '.page-nav-container',
      offset: 100
    });

    //Easy scrolling (a link to #section will scroll to #section)
    $('.nav a[href^="#"]').on('click',function (e) {
      e.preventDefault();

      var target = this.hash;
      var $target = $(target);

      if ($target.length) {
        $('html, body').stop().animate({
            'scrollTop': $target.offset().top - 30
        }, 300, 'swing', function() {
          window.location.hash = target;
        });
      }
    });

    $('.collapse')
      .on('shown.bs.collapse', function() {
        var $toggle = $('a.show-more[href="#' + this.id + '"]');
        $toggle.find('.fa').removeClass('fa-plus').addClass('fa-minus');
        // send google analytics event
        ga('send', 'event', 'show-more', this.id);
      })
      .on('hidden.bs.collapse', function() {
        var $toggle = $('a.show-more[href="#' + this.id + '"]');
        $toggle.find('.fa').removeClass('fa-minus').addClass('fa-plus');
      });

    // setup 'email municipality' link, by choosing all the emails of the first two people
    var emails = $('#who-runs .contact-details')
      .slice(0, 2)
      .find('a[href^="mailto:"]')
      .map(function() { return this.href.split(':')[1]; });
    emails = _.compact(_.uniq(emails));

    if (emails.length > 0) {
      var body = 'You can explore Municipal Finance for ' + profileData.geography.name + ' at ' + window.location;

      var url = ('mailto:' +
        emails.join(';') +
        '?cc=feedback@municipalmoney.gov.za' +
        '&subject=' + encodeURIComponent('Feedback via Municipal Money') +
                 '&body=\n\n\n' + encodeURIComponent(body));
      $('a.send-email').attr('href', url);
    } else {
      $('a.send-email').addClass('disabled');
    }
  }
});
