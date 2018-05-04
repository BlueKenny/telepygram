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
            listeChat.currentIndex = listeChat.count - 1
        }


    }

    Label {
        text: "<"
        x: 20
        y: 20
        font.pixelSize: mainWindow.width / 20

    }
    Label {
        id: nameChatPartner
        text: "..."
        x: mainWindow.width / 2 - width / 2
        y: 20
        font.pixelSize: mainWindow.width / 20
    }
    MouseArea {
        id: backMouseArea
        width: window.width
        height: nameChatPartner.height + 40
        onClicked: {
            view.push(frameDialogs)
            python.call('Main.main.getDialogs', [], function () {});
        }
    }


    ListView {
        id: listeChat
        y: backMouseArea.height * 2//150
        x: 20
        width: window.width - 2 * x
        height: window.height - y - textInput.height
        highlightFollowsCurrentItem: true
        highlightMoveDuration: 100
        //highlight: Rectangle { color: "lightsteelblue"; width: window.width}

        ListModel {
            id: chatModel
        }

        Component {
            id: chatDelegate
            Item {
                id: itemListe
                x: parent.x
                width: parent.width
                height: textChatText.height + window.height / 20

                MouseArea {
                    anchors.fill: parent
                    onClicked: liste.currentIndex = index
                }
                Text {
                    id: textChatText
                    text: sender + ":\n" + chattext
                    color: out ? "orange" : "blue"
                    x: parent.x
                    width: parent.width
                    font.pixelSize: mainWindow.width / 25
                    horizontalAlignment: out ? Text.AlignRight : Text.AlignLeft
                    wrapMode: Text.WordWrap
                }
            }
        }

        model: chatModel
        delegate: chatDelegate
    }

    TextField {
        id: textInput
        width: mainWindow.width
        height: mainWindow.height / 10
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
