import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

Rectangle {
    id: window
    height: mainWindow.height
    width: mainWindow.width

    Label {
        id: labelSelectTitle
        text: "Please ENTER your Phone number"
        font.pixelSize: mainWindow.width / 50
        x: window.width / 2 - width / 2
        y: window.height / 5
    }
    TextField {
        id: textPhoneNumberNum
        width: window.width / 3
        height: window.height / 15
        x: window.width / 2 - width / 2
        y: window.height / 2 - height / 2
        onAccepted: {
            python.call('Main.main.setPhoneNumber', [text], function () {});
        }
    }
}
