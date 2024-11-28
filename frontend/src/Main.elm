port module Main exposing (main)
import Browser
import Browser.Events


import Html exposing (Html, div)
import Html.Events exposing (on)
import Html.Attributes exposing (class)
import Json.Decode
import Json.Encode
import Json.Decode exposing (Error(..))


main =
  Browser.element { init = init, view = view, update = update, subscriptions = subscriptions }

-- State
type alias Model = {
  snakePosition: (Int, Int),
  area: Int,
  direction: Direction,
  foodPosition: (Int, Int)
  }
type Direction = Up | Down | Left | Right
type alias WebSocketMessage = {
  messageType: String,
  position: (Int, Int),
  message: Maybe String
  }

type Payload = MovePayload {position: (Int, Int), direction: Direction} | ClickPayload {position: (Int, Int)}
-- Init
init: () -> (Model, Cmd Msg)
init _ = ( { snakePosition = (0,0), area = 500, direction = Up, foodPosition = (0,0) }, Cmd.none )


-- Update logic
type Msg = PressKey String | ClickedPosition (Int, Int) | MessageReceived String

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    PressKey key ->
      case key of
        "ArrowUp" -> (model,sendMessage (encodeMoveMessage {position = model.snakePosition, direction = Up}))
        "ArrowDown" -> (model,sendMessage (encodeMoveMessage {position = model.snakePosition, direction = Down}))
        "ArrowLeft" -> (model,sendMessage (encodeMoveMessage {position = model.snakePosition, direction = Left}))
        "ArrowRight" -> (model,sendMessage (encodeMoveMessage {position = model.snakePosition, direction = Right}))
        _ -> (model, Cmd.none)
    ClickedPosition (x, y) ->
      ( model , sendMessage (encodeClickMessage {position = (x, y)}))
    MessageReceived wsMessage ->
      case Json.Decode.decodeString wsMessageDecoder wsMessage of
        Ok data ->
          case data.messageType of
            "move" ->
              ({model | snakePosition = data.position}, Cmd.none)
            "click" ->
              ({model | foodPosition = data.position}, Cmd.none)
            _ ->
              (model, Cmd.none)
        Err _ ->
          (model, Cmd.none)
-- Subscriptions
subscriptions : Model -> Sub Msg
subscriptions _ =
  Sub.batch [
    Browser.Events.onKeyDown (Json.Decode.map PressKey keyDecoder),
    messageReceiver MessageReceived
  ]

-- Decoders
keyDecoder : Json.Decode.Decoder String
keyDecoder =
    Json.Decode.field "key" Json.Decode.string

clickDecoder : Json.Decode.Decoder Msg
clickDecoder =
  Json.Decode.map2 Tuple.pair (Json.Decode.field "offsetX" Json.Decode.int) (Json.Decode.field "offsetY" Json.Decode.int) |> Json.Decode.map ClickedPosition

wsMessageDecoder : Json.Decode.Decoder WebSocketMessage
wsMessageDecoder =
  Json.Decode.map3 WebSocketMessage
    (Json.Decode.field "type" Json.Decode.string)
    (Json.Decode.field "position" (Json.Decode.map2 Tuple.pair (Json.Decode.field "x" Json.Decode.int) (Json.Decode.field "y" Json.Decode.int)))
    (Json.Decode.maybe (Json.Decode.field "message" Json.Decode.string))
-- Encoders
encoderKey: Direction -> String
encoderKey direction =
  case direction of
    Up -> "up"
    Down -> "down"
    Left -> "left"
    Right -> "right"

encodePosition: (Int, Int) -> Json.Encode.Value
encodePosition (x,y) =
  Json.Encode.object [
    ("x", Json.Encode.int x),
    ("y", Json.Encode.int y)
  ]

encodePayload: Payload -> Json.Encode.Value
encodePayload payload =
  case payload of
    MovePayload {position, direction} ->
      Json.Encode.object [
        ("position", encodePosition position),
        ("direction", Json.Encode.string (encoderKey direction))
      ]
    ClickPayload {position} ->
      Json.Encode.object [
        ("position", encodePosition position)
      ]

encodeMoveMessage: {position: (Int, Int), direction: Direction} -> String
encodeMoveMessage {position, direction} =
  Json.Encode.object [
    ("type", Json.Encode.string "move"),
    ("payload", encodePayload (MovePayload {position=position, direction=direction}))
  ] |> Json.Encode.encode 0

encodeClickMessage: {position: (Int, Int)} -> String
encodeClickMessage {position} =
  Json.Encode.object [
    ("type", Json.Encode.string "click"),
    ("payload", encodePayload (ClickPayload {position=position}))
  ] |> Json.Encode.encode 0

-- Ports
port sendMessage : String -> Cmd msg
port messageReceiver : (String -> msg) -> Sub msg

-- View
view : Model -> Html Msg
view model =
    div [ class "container mx-auto h-screen place-content-center" ] [
      div [class ("bg-blue-500 mx-auto relative w-[" ++ String.fromInt model.area ++ "px] h-[" ++ String.fromInt model.area ++ "px]"), Html.Events.on "click" clickDecoder   ] [
        div [class ("absolute top-[" ++ String.fromInt (Tuple.second model.snakePosition) ++ "px] left-[" ++ String.fromInt (Tuple.first model.snakePosition) ++ "px] w-10 h-10 bg-red-500") ] [],
        div [class ("absolute top-[" ++ String.fromInt (Tuple.second model.foodPosition) ++ "px] left-[" ++ String.fromInt (Tuple.first model.foodPosition) ++ "px] w-3 h-3 bg-green-500") ] []
      ]
     ]
