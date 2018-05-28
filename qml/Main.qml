import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2
//import Ubuntu.Components 1.3

//import Ubuntu.PushNotifications 0.1

ApplicationWindow {
//Rectangle {
    id: mainWindow
    height: 500
    width: 500
    title: qsTr("Telepygram")
/*
    PushClient {
        id: pushClient
        Component.onCompleted: {
            notificationsChanged.connect(messageList.handle_notifications)
            error.connect(messageList.handle_error)
        }
        appId: "telepygram.bluekenny_telepygram"
    }*/

    Item {
        id: vars
        property string testString: ""
        property bool keyboardVisible: true
        property bool onlineStatus: false
        property string backgroundColorPanel: "#38393C"
        property string backgroundColor: "#4a4b4f"
        property string textColor: "#F5F5F5"

    }

    function busy(status) {
        busyindicator.visible = status
    }

    function changeOnlineStatus(status) {
        vars.onlineStatus = status
    }

    function changeFrame(frameSelect) {
        if (frameSelect === "PhoneCall") {
            timeDialogs.running = false
            timeChat.running = false
            timeSending.running = false
            view.push(framePhoneCall)
        }
        if (frameSelect === "Phone") {
            timeDialogs.running = false
            timeChat.running = false
            timeSending.running = false
            view.push(framePhoneNumber)
        }
        if (frameSelect === "Code") {
            timeDialogs.running = false
            timeChat.running = false
            timeSending.running = false
            view.push(framePhoneCode)
        }
        if (frameSelect === "Dialogs") {
            timeDialogs.running = true
            timeChat.running = false
            timeSending.running = true
            view.push(frameDialogs)
            python.call('Main.main.reloadDialogs', [], function () {});
        }
        if (frameSelect === "Chat") {
            timeDialogs.running = false
            timeChat.running = true
            timeSending.running = true
            view.push(frameChat)
            python.call('Main.main.reloadChat', [true], function () {});
        }
    }

    KeyboardRectangle {
        id: kbdRect
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        onScaleChanged: {
            console.warn("Keyboard changed")
        }
    }

    Timer {
        id: timeDialogs
        interval: 5000; running: true; repeat: true
        onTriggered: {
            console.warn("timeDialogs")
            python.call('Main.main.reloadDialogs', [], function () {});
        }
    }
    Timer {
        id: timeChat
        interval: 5000; running: false; repeat: true
        onTriggered: {
            console.warn("timeChat")
            python.call('Main.main.reloadChat', [true], function () {});
        }
    }
    Timer {
        id: timeSending
        interval: 5000; running: true; repeat: true
        onTriggered: {
            console.warn("timeSending")
            python.call('Main.main.trySending', [], function () {});
        }
    }

    Timer {
        id: timeCalls
        interval: 1000; running: false; repeat: true
        onTriggered: {
            console.warn("timeCalls")
            python.call('Main.main.receivedCall', [], function () {});
        }
    }

    BusyIndicator {
        id: busyindicator
        running: true //image.status === Image.Loadings
        x: mainWindow.width / 2
        y: mainWindow.height / 2
    }

    StackView {
        id: view

        delegate: StackViewDelegate {

            function transitionFinished(properties)
            {
                properties.exitItem.opacity = 1
            }

            pushTransition: StackViewTransition {
                PropertyAnimation {
                    target: enterItem
                    property: "opacity"
                    from: 0
                    to: 1
                    duration: 200
                }
                PropertyAnimation {
                    target: exitItem
                    property: "opacity"
                    from: 1
                    to: 0
                    duration: 200
                }
            }
        }

        initialItem: frameDialogs
        anchors.fill: parent

        Component {
            id: frameDialogs
            Dialogs {id: dialogsWindow}
        }
        Component {
            id: framePhoneNumber
            PhoneNumber {}
        }
        Component {
            id: framePhoneCode
            PhoneCode {}
        }
        Component {
            id: frameChat
            Chat {}
        }
        Component {
            id: framePhoneCall
            PhoneCall {}
        }
    }

    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('./'));
            importModule('Main', function () {});

            //
            //setHandler("busy", busy);
            setHandler("changeFrame", changeFrame);

            setHandler("onlineStatus", changeOnlineStatus);

            //setHandler("antwortGetDialogs", view.currentItem.antwortGetDialogs);
        }
    }
}
