var concat = require('gulp-concat');
var gulp = require('gulp');
var gulpif = require('gulp-if');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');


var config = {
    js: {
        src: [
            // Modernizr
            'django_backend/static/django_backend/libs/modernizr/modernizr.js',

            // jQuery
            'django_backend/static/django_backend/libs/jquery/dist/jquery.min.js',
            'django_backend/static/django_backend/libs/jquery-ui/ui/minified/jquery-ui.min.js',

            // Bootstrap
            'django_backend/static/django_backend/libs/bootstrap-sass/assets/javascripts/bootstrap.min.js',
            'django_backend/static/django_backend/libs/bootstrap-tab-history/vendor/assets/javascripts/bootstrap-tab-history.js',

            // Stapes
            'django_backend/static/django_backend/libs/stapes/stapes.min.js',

            // RequireJS
            'django_backend/static/django_backend/libs/requirejs/require.js',

            // Backend
            'django_backend/static/django_backend/js/**/*.js',
        ],
        watch: [
            'django_backend/static/django_backend/js/**/*.js',
        ]
    },
    sass: {
        src: [
            'django_backend/static/django_backend/scss/django_backend.scss',
            'django_backend/static/django_backend/scss/jquery-ui.scss',
        ],
        watch: [
            'django_backend/static/django_backend/scss/**/*.scss',
        ]
    },
    dev: false
};


gulp.task('js', function () {
    return gulp.src(config.js.src)
        .pipe(gulpif(config.dev, sourcemaps.init()))
        .pipe(concat('django_backend.js'))
        .pipe(gulpif(!config.dev, uglify()))
        .pipe(gulpif(config.dev, sourcemaps.write()))
        .pipe(gulp.dest('django_backend/static/django_backend/dist/'));
});


gulp.task('js:watch', ['js'], function () {
    gulp.watch(config.js.watch, ['js']);
});


gulp.task('sass', function () {
    return gulp.src(config.sass.src)
        .pipe(gulpif(config.dev, sourcemaps.init()))
        .pipe(gulpif(!config.dev, sass({
            outputStyle: 'compressed',
        }).on('error', sass.logError)))
        .pipe(gulpif(config.dev, sass({}).on('error', sass.logError)))
        .pipe(gulpif(config.dev, sourcemaps.write()))
        .pipe(gulp.dest('django_backend/static/django_backend/dist/'));
});


gulp.task('sass:watch', ['sass'], function () {
    gulp.watch(config.sass.watch, ['sass']);
});


gulp.task('dev', function () {
    config.dev = true;
});


gulp.task('build', ['js', 'sass'], function () {

});


gulp.task('watch', ['js:watch', 'sass:watch'], function () {

});


gulp.task('default', ['build'], function () {

});
