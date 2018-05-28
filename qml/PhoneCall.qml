import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

Rectangle {
    id: window
    height: mainWindow.height
    width: mainWindow.width
    color: vars.backgroundColor

    Label {
        id: labelSelectTitle
        text: "You missed a Call\n This is a work in Progress for phone Calls"
        font.pixelSize: mainWindow.width / 20
        x: window.width / 2 - width / 2
        y: window.height / 5
        color: vars.textColor
    }
}
