import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

Rectangle {
    id: window
    height: mainWindow.height
    width: mainWindow.width

    Label {
        id: labelSelectTitle
        text: "Telegram have send you a \n verification code,\n please ENTER it"
        font.pixelSize: mainWindow.width / 20
        x: window.width / 2 - width / 2
        y: window.height / 5
    }
    TextField {
        id: textPhoneNumberNum
        width: window.width
        height: window.height / 12
        x: window.width / 2 - width / 2
        y: window.height / 2 - height / 2
        font.pixelSize: mainWindow.width / 20
        inputMethodHints: Qt.ImhDigitsOnly
        horizontalAlignment: TextEdit.AlignHCenter
        onAccepted: {
            python.call('Main.main.setPhoneCode', [text], function () {});
        }
    }
}
