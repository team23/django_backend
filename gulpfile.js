var gulp = require('gulp');
var sass = require('gulp-sass');


var config = {
    sass: {
        src: [
            'django_backend/static/django_backend/scss/django_backend.scss',
            'django_backend/static/django_backend/scss/jquery-ui.scss',
        ],
        watch: [
            'django_backend/static/django_backend/scss/**/*.scss',
        ]
    }
};


gulp.task('build', function () {
    return gulp.src(config.sass.src)
        .pipe(sass())
        .pipe(gulp.dest('django_backend/static/django_backend/css/'));
});


gulp.task('watch', function () {
    gulp.watch(config.sass.watch, ['build']);
});


gulp.task('default', ['build'], function () {

});
