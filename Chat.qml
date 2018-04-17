import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

Rectangle {
    id: window
    height: mainWindow.height
    width: mainWindow.width


    function antwortGetChat(item, username) {
        console.warn("QML antwortGetChat")
        nameChatPartner.text = username

        chatModel.clear()
        for (var i=0; i<item.length; i++) {
            chatModel.append(item[i]);
        }
    }

    Label {
        id: nameChatPartner
        text: "..."
        x: mainWindow.width / 2 - width / 2
        font.pixelSize: mainWindow.width / 20
    }


    ListView {
        id: listeChat
        y: window.height / 10
        width: window.width
        height: window.height * 0.7

        ListModel {
            id: chatModel
        }

        Component {
            id: chatDelegate
            Item {
                id: itemListe
                width: window.width
                height: window.height/6
                MouseArea {
                    anchors.fill: parent
                    onClicked: liste.currentIndex = index
                }
                Label {
                    text: chattext
                    x: window.width / 2 - width / 2
                    font.pixelSize: mainWindow.width / 20
                }
            }
        }

        model: chatModel
        delegate: chatDelegate
    }

    TextField {
        id: textInput
        width: mainWindow.width
        font.pixelSize: mainWindow.width / 20
        y: mainWindow.height - height
        onAccepted: {
            python.call('Main.main.sendChat', [text], function () {text = ""});
        }
    }

    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('./'));
            importModule('Main', function () {});

            setHandler("antwortGetChat", antwortGetChat)
        }
    }

}
