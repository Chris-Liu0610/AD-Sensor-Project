


```mermaid
classDiagram


MainPresenter -- LEDPresenter
MainPresenter -- CameraPresenter

PersonalWindow -- MainPresenter
ArduionController -- MainPresenter
ArduionController .. LEDPresenter

ArduionController .. CameraPresenter
CameraDevice -- CameraPresenter
VideoRecorder -- CameraPresenter
LEDPresenter -- LEDWindow
CameraPresenter -- CameraWindow

Analyser -- AalysisPresenter
AnalysisWindow -- AalysisPresenter



class ArduionController {
    +finish?
}




```