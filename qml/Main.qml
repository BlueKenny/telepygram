import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2
//import Ubuntu.Components 1.3

ApplicationWindow {
//Rectangle {
    id: mainWindow
    height: 500
    width: 500
    title: qsTr("Telepygram")

    Item {
        id: vars
        property string testString: ""
    }

    function busy(status) {
        busyindicator.visible = status
    }

    function changeFrame(frameSelect) {
        if (frameSelect === "PhoneCall") {
            timeDialogs.running = false
            timeChat.running = false
            view.push(framePhoneCall)
        }
        if (frameSelect === "Phone") {
            timeDialogs.running = false
            timeChat.running = false
            view.push(framePhoneNumber)
        }
        if (frameSelect === "Code") {
            timeDialogs.running = false
            timeChat.running = false
            view.push(framePhoneCode)
        }
        if (frameSelect === "Dialogs") {
            timeDialogs.running = true
            timeChat.running = false
            view.push(frameDialogs)
            python.call('Main.main.reloadDialogs', [], function () {});
        }
        if (frameSelect === "Chat") {
            timeDialogs.running = false
            timeChat.running = true
            view.push(frameChat)
            python.call('Main.main.reloadChat', [true], function () {});
        }
    }

    Timer {
        id: timeDialogs
        interval: 10000; running: true; repeat: true
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

            //setHandler("antwortGetDialogs", view.currentItem.antwortGetDialogs);
        }
    }
}
