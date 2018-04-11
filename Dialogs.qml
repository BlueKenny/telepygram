import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

Rectangle {
    id: window
    height: mainWindow.height
    width: mainWindow.width

    Label {
        id: labelSelectTitle
        text: "Telepygram"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 2 - width / 2
    }
    Button {
        id: buttonKunden
        text: "Kunden"
        width: vars.isPhone ? window.width / 2 : window.width / 5
        height: window.height / 5
        x: window.width / 3 - width / 2
        y: window.height / 5 * 3 - height / 2
        onClicked: {
            view.push(frameKundenSuchen)
        }
    }
}