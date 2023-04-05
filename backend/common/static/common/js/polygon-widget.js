(function ($) {
    function init() {
        var $block = $('.js-sc');

        const act = '_active';

        if (!$block.length) return;

        // Elements

        var $input = $('.js-sc-i');

        var $wrapper = $('.js-sc-wrapper');
        var $svg = $('.js-sc-svg');
        var $polygon = $('.js-sc-polygon');

        // Controls

        var $tagOutput = $('.js-sc-tag');
        var $pointsOutput = $('.js-sc-points');

        var $undo = $('.js-sc-undo');
        var $refresh = $('.js-sc-refresh');

        // State

        var points = [];
        var tag = true;

        // Sizes

        var bw = $wrapper.innerWidth();
        var ot = $wrapper.offset().top;
        var ol = $wrapper.offset().left;
        var iw = $svg[0].getAttribute('viewBox').split(' ')[2];
        var diff = iw / bw;

        // Events

        $svg.on('click', clickSignal);

        $refresh.on('click', refreshSignal);
        $undo.on('click', undoSignal);

        $tagOutput.on('click', tagOutputSignal);
        $pointsOutput.on('click', pointsOutputSignal);

        // Signals && Methods

        function clickSignal(e) {
            var left = e.pageX;
            var top = e.pageY;

            var t_point = top - ot;
            var l_point = left - ol;

            var svg_t_point = Math.round((t_point * diff) * 1000) / 1000;
            var svg_l_point = Math.round((l_point * diff) * 1000) / 1000;

            points.push('' + svg_l_point + ',' + svg_t_point + '');

            makerString();
        }

        function refreshSignal() {
            points = [].concat.apply([]);
            makerString();
        }

        function undoSignal() {
            points.pop();
            makerString();
        }

        function tagOutputSignal() {
            tag = true;

            $pointsOutput.removeClass(act);
            $tagOutput.addClass(act);

            makerString();
        }

        function pointsOutputSignal() {
            tag = false;

            $tagOutput.removeClass(act);
            $pointsOutput.addClass(act);

            makerString();
        }

        function makerString() {
            let str = '';

            for (var i = 0; i < points.length; i++) {
                var point = points[i];

                str += point + ' ';
            }

            updateInput(str);
            updatePolygon(str);
        }

        function updateInput(str) {
            tag
                ? $input.val((str.replace(' ', '') !== '') ? '<polygon points="' + str + '"></polygon>' : '')
                : $input.val(str);
        }

        function updatePolygon(str) {
            $polygon.attr('points', str);
        }
    }

    $(document).ready(function () {
        init();
    });
})(window.jQuery || django.jQuery);;
