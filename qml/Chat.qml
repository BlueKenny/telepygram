import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2
//import QtQuick.Controls.Styles 1.4
import QtQuick.Dialogs 1.0
import QtGraphicalEffects 1.0

import QtMultimedia 5.4

//import Dekko.Notify 1.0

Rectangle {
    id: window
    height: mainWindow.height
    color: vars.backgroundColor
    //height:  Qt.inputMethod.visible ? mainWindow.height * 0.55 : mainWindow.height

/*
    anchors {
        left: parent.left
        top: parent.top
        right: parent.right
        // anchor to the top of KeyboardRectangle
        // this ensures pages are always above the OSK
        // Basically the same as anchorToKeyboard
        bottom: kbdRect.top
    }*/

/*
    Notify {
        id: notify
    }*/


    function antwortGetChat(item, username) {
        console.warn("QML antwortGetChat")
        nameChatPartner.text = username

        //chatModel.clear()
        for (var i=0; i<item.length; i++) {
            //chatModel.append(item[i]);
            chatModel.set(i, item[i]);
        }

        //notify.send("Test")

        //if (listeChat.visibleArea.yPosition == listeChat.) {
        //    listeChat.currentIndex = listeChat.count - 1
        //}
    }

    Rectangle { // to hide the ListView in the Top
        id: topPanelChat
        width: window.width
        height: nameChatPartner.height * 2 + 40
        color: vars.backgroundColorPanel
        border.width: 2
        z: 1

        Label {
            id: backLabelChat
            text: "<"
            x: 20
            y: 20
            font.pixelSize: nameChatPartner.font.pixelSize
            color: vars.textColor
        }
        Label {
            id: nameChatPartner
            text: "..."
            x: mainWindow.width / 2 - width / 2
            y: 20
            font.pixelSize: mainWindow.width / 30
            color: vars.textColor
        }
        MouseArea {
            id: backMouseArea
            anchors.fill: topPanelChat
            onClicked: {
                view.push(frameDialogs)
                python.call('Main.main.getDialogs', [], function () {});
            }
        }
        Label {
            id: labelStatus
            text: vars.onlineStatus ? "You are\nOnline" : "You are\nOffline"
            color: vars.onlineStatus ? "green" : "red"
            x: window.width - width
            font.pixelSize: nameChatPartner.font.pixelSize
            transform: Rotation { origin.x: 0; origin.y: 0; axis { x: 1; y: 1; z: 1 } angle: 45 }
        }
    }

    ListView {
        id: listeChat
        y: backMouseArea.height
        x: 20
        z: topPanelChat.z - 1
        width: window.width - 2 * x
        height: window.height - y - textInput.height
        highlightFollowsCurrentItem: true
        highlightMoveDuration: 100
        //highlight: Rectangle { color: "lightsteelblue"; width: window.width}

        onMovementEnded: {
            console.warn("Move Stoped")
            console.warn("listeChat visibleArea.yPosition: " + listeChat.visibleArea.yPosition)
            if (listeChat.visibleArea.yPosition == 0) {
                // if Scroll to Start then Download More Messages

                python.call('Main.main.reloadChat', [false], function () {});

            }
        }

        ListModel {
            id: chatModel
        }

        Component {
            id: chatDelegate

            Item {
                id: itemListe
                x: parent.x
                width: parent.width
                height: textChatText.height + imageChat.height + window.height / 20
/*
                Image {
                    id: imageChat
                    x: parent.width / 2 - width / 2
                    y: textChatText.height
                    width: parent.width / 2
                    height: with_media ? width : 0
                    source: media
                }

                Text {//Image {
                    id: textChatText
                    //source: "icons/bluble-right.png"
                    //asynchronous: true
                    //sourceSize: Qt.size(parent.width, parent.height)
                    //smooth: true
                    visible: false
                    text: sender + ":\n" + chattext
                    x: parent.x + 10
                    color: vars.textColor
                    width: parent.width - 20
                    font.pixelSize: mainWindow.width / 25
                    horizontalAlignment: out ? Text.AlignRight : Text.AlignLeft
                    wrapMode: Text.WordWrap

                }
                Image {
                    id: mask
                    source: "icons/bluble-right.png"
                    sourceSize: Qt.size(parent.width, parent.height)
                    smooth: true
                    visible: false
                }
                OpacityMask {
                    anchors.fill: textChatText
                    source: textChatText
                    maskSource: mask
                }*/

                Rectangle {
                    height: parent.height - 10
                    width: parent.width - 10
                    border.width: 1
                    border.color: read ? "green" : "red"
                    color: out ? "#2C3349" : "#1D2C58"
                    radius: 30

                    //transform: Rotation { origin.x: 0; origin.y: 0; axis { x: 1; y: 1; z: 1 } angle: 45 }

                    Rectangle {
                        id: mediaPlayer
                        x: parent.width / 2 - width / 2
                        y: textChatText.height
                        width: parent.width / 2
                        height: with_media ? width : 0

                        Video {
                            id: videoChat
                            anchors.fill: parent
                            source: media_is_video ? media : ""
                            z: media_is_video ? parent.z : parent.z - 1
                            MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    console.warn("Start Video")
                                    videoChat.play()
                                }
                            }
                        }
                        Image {
                            id: imageChat
                            anchors.fill: parent
                            z: media_is_image ? parent.z : parent.z - 1
                            source: media_is_image ? media : ""
                            asynchronous: true
                        }
                    }

                    Text {
                        id: textChatText
                        text: sender + ":\n" + chattext
                        color: vars.textColor
                        x: parent.x + 10
                        y: window.height / 40
                        width: parent.width - 20
                        font.pixelSize: nameChatPartner.font.pixelSize
                        horizontalAlignment: out ? Text.AlignRight : Text.AlignLeft
                        wrapMode: Text.WordWrap
                    }
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
        font.pixelSize: nameChatPartner.font.pixelSize
        z: listeChat.z + 1
        y: window.height - height/*
        style: TextFieldStyle {
            textColor: vars.textColor
            background: Rectangle { color: vars.backgroundColorPanel }
        }*/
        onAccepted: {
            python.call('Main.main.sendChat', [text], function () {text = ""});
            window.height = mainWindow.height
        }
        on__ContentWidthChanged: {
            window.height = mainWindow.height * 0.55
        }
        onEditingFinished: {
            window.height = mainWindow.height
        }
        onCursorPositionChanged: {
            window.height = mainWindow.height * 0.55
        }
    }/*
    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        folder: shortcuts.home
        selectExisting: true
        onAccepted: {
            console.log("You chose: " + fileDialog.fileUrls)
        }
        onRejected: {
            console.log("Canceled")
        }
        Component.onCompleted: visible = true
    }*/

    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('./'));
            importModule('Main', function () {});

            setHandler("antwortGetChat", antwortGetChat)
        }
    }

}
