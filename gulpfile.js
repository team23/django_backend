var gulp = require('gulp');
var gulpif = require('gulp-if');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');


var config = {
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


gulp.task('sass', function () {
    return gulp.src(config.sass.src)
        .pipe(gulpif(config.dev, sourcemaps.init()))
        .pipe(sass({
            outputStyle: 'compressed',
        }).on('error', sass.logError))
        .pipe(gulpif(config.dev, sourcemaps.write()))
        .pipe(gulp.dest('django_backend/static/django_backend/css/'));
});


gulp.task('sass:watch', function () {
    gulp.watch(config.sass.watch, ['sass']);
});


gulp.task('build', ['sass'], function () {

});


gulp.task('dev', function () {
    config.dev = true;
});


gulp.task('watch', ['sass:watch'], function () {

});


gulp.task('default', ['build'], function () {

});
