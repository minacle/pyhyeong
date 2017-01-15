#!/usr/bin/env python3.6
"""
난해한 혀엉... 언어 v0.4.0
<https://gist.github.com/xnuk/d9f883ede568d97caa158255e4b4d069>

이 구현체는 위에 표기된 버전의 문서를 기반으로 합니다.
"""

ELLIPSES = ["…", "⋯", "⋮"]  # U+2026, U+22EF, U+22EE
DOT = "."  # U+2E

HANGUL_FIRST = "가"  # U+AC00
HANGUL_LAST = "힣"  # U+D7A3

QUESTION_MARK = "?"  # U+3F
EXCLAMATION_MARK = "!"  # U+21

HEARTS = [
    "♥", "❤", "💕", "💖",  # U+2665, U+2764, U+1F495, U+1F496
    "💗", "💘", "💙", "💚",  # U+1F497, U+1F498, U+1F499, U+1F49A
    "💛", "💜", "💝",  # U+1F49B, U+1F49C, U+1F49D
]
EMPTY_HEART = "♡"  # U+2661

NAN_STRING = "너무 커엇..."


class Hyeong:
    """
    혀엉... 클래스예요...♥

    아래 명령의 이름은 ISO/TR 11941:1196 Method 1을 따라요...
    - 형: hyeong
    - 항: hang
    - 핫: has
    - 흣: heus
    - 흡: heup
    - 흑: heuk

    그리고 하트랑 물음표랑 느낌표 명령의 이름은 아래와 같아요... 흐읏!
    - ♥, ❤, 💕, 💖, 💗, 💘, 💙, 💚, 💛, 💜, 💝: heart
    - ♡: empty_heart
    - ?: question_mark
    - !: exclamation_mark
    """

    _HA = "하"
    _HANG = "항"
    _ANG = "앙"
    _HAS = "핫"
    _AS = "앗"

    _HYEO = "혀"
    _HYEONG = "형"
    _EONG = "엉"

    _HEU = "흐"
    _HEUK = "흑"
    _EUK = "윽"
    _HEUP = "흡"
    _EUP = "읍"
    _HEUS = "흣"
    _EUS = "읏"

    def hyeong(self, hangul_count, dot_count, *args,
               full_command=None, line=None, char=None):
        """
        `형`, `혀엉`, `혀어엉`, `혀어어엉`… : 글자 수와 마침표 개수를
        곱한 값을 현재 스택에 저장합니다.

        - 예를 들어 `혀어엉....`은 `12`를 현재 스택에 넣습니다.
        - `혀`와 `엉` 사이에 `엉`을 제외한 한글 음절 문자를 추가적으로
          넣어 글자 수를 늘릴 수 있습니다.
        """
        if self.debug:
            print(f"{line}:{char} {full_command}")
            print(f" -> {Hyeong._HYEONG}({hangul_count}, {dot_count})")

        numerator = hangul_count * dot_count
        denominator = 1

        if self.debug:
            print(f"    value = {numerator}/{denominator}")
            print(f"     -> {numerator // denominator}")
            print(f"    push value to:{self.cursor}")
            print(f"     -> ({numerator}/{denominator})", end="")
            for item in self._stack_peek(3):
                if item is not None:
                    if item == (None, ):
                        print(f", NaN", end="")
                    else:
                        print(f", ({item[0]}/{item[1]})", end="")
            count = self._stack_count()
            if count - 3 > 0:
                print(f", ...", end="")
            print()
        self._stack_push([(numerator, denominator)])
        if self.debug:
            print()

    def hang(self, hangul_count, dot_count, *args,
             full_command=None, line=None, char=None):
        """
        `항`, `하앙`, `하아앙`, `하아아앙`… : 현재 스택에서 글자 수만큼
        뽑아 모두 더하여 마침표 개수에 해당하는 스택에 넣습니다.

        - 예를 들어 `하아앙....`은 원소 세 개를 뽑아 모두 더한 다음 그
          값을 4번 스택에 넣습니다.
        - `하`와 `앙` 사이에 `앙`을 제외한 한글 음절 문자를 추가적으로
          넣어 글자 수를 늘릴 수 있습니다.
        """
        if self.debug:
            print(f"{line}:{char} {full_command}")
            print(f" -> {Hyeong._HANG}({hangul_count}, {dot_count})")

        numerator = 0
        denominator = 1
        nan = False

        for value in self._stack_pop(hangul_count):
            if value is not None:
                if value != (None, ):
                    temp = reduce((numerator, denominator), value)
                    numerator = temp[0][0] + temp[1][0]
                    denominator = temp[1][1]
                    numerator, denominator = reduce((numerator, denominator))
                else:
                    nan = True

        if nan:
            if self.debug:
                print(f"    value = NaN")
                print(f"     -> {NAN_STRING}")
                print(f"    push value to:{dot_count}")
            self._stack_push([(None, )], dot_count)
        else:
            if self.debug:
                print(f"    value = {numerator}/{denominator}")
                print(f"     -> {numerator // denominator}")
                print(f"    push value to:{dot_count}")
            self._stack_push([(numerator, denominator)], dot_count)
        if self.debug:
            print()

    def has(self, hangul_count, dot_count, *args,
            full_command=None, line=None, char=None):
        """
        `핫`, `하앗`, `하아앗`, `하아아앗`… : 현재 스택에서 글자 수만큼
        뽑아 모두 곱하여 마침표 개수에 해당하는 스택에 넣습니다.

        - 예를 들어 `하아앗....`은 원소 세 개를 뽑아 모두 곱한 다음 그
          값을 4번 스택에 넣습니다.
        - `하`와 `앗` 사이에 `앗`을 제외한 한글 음절 문자를 추가적으로
          넣어 글자 수를 늘릴 수 있습니다.
        """
        if self.debug:
            print(f"{line}:{char} {full_command}")
            print(f" -> {Hyeong._HAS}({hangul_count}, {dot_count})")

        numerator = denominator = 0
        nan = False

        for value in self._stack_pop(hangul_count):
            if value is not None:
                if value != (None, ):
                    if denominator == 0:
                        numerator, denominator = value
                    else:
                        numerator *= value[0]
                        denominator *= value[1]
                        numerator, denominator = reduce((numerator, denominator))
                else:
                    nan = True

        if nan:
            if self.debug:
                print(f"    value = NaN")
                print(f"     -> {NAN_STRING}")
                print(f"    push value to:{dot_count}")
            self._stack_push([(None, )], dot_count)
        else:
            if self.debug:
                print(f"    value = {numerator}/{denominator}")
                print(f"     -> {numerator // denominator}")
                print(f"    push value to:{dot_count}")
            self._stack_push([(numerator, denominator)], dot_count)
        if self.debug:
            print()

    def heus(self, hangul_count, dot_count, *args,
             full_command=None, line=None, char=None):
        """
        `흣`, `흐읏` , `흐으읏`, `흐으으읏`… : 스택의 위쪽에서 글자
        수만큼의 원소들의 부호를 바꾼 후 그 합을 마침표 개수에 해당하는
        스택에 넣습니다.

        - 예로 스택이 `1 0 -3 4`순으로 있고 `4`가 다음에 뽑힐 원소인
          상태에서 `흐읏...`을 하면 스택은 `1 0 3 -4`가 되고, 3번 스택에
          `-1`을 넣습니다.
        - `흐`와 `읏` 사이에 `읏`을 제외한 한글 음절 문자를 추가적으로
          넣어 글자 수를 늘릴 수 있습니다.
        """
        if self.debug:
            print(f"{line}:{char} {full_command}")
            print(f" -> {Hyeong._HEUS}({hangul_count}, {dot_count})")

        numerator = denominator = 0
        nan = False
        val = []

        for value in self._stack_peek(hangul_count):
            if value is not None:
                if value != (None, ):
                    val.append((-value[0], value[1]))
                    if denominator == 0:
                        numerator, denominator = val[-1]
                    else:
                        temp = reduce((numerator, denominator), val[-1])
                        numerator = temp[0][0] + temp[1][0]
                        numerator, denominator = reduce((numerator, temp[1][1]))
                else:
                    val.append((None, ))
                    nan = True

        self._stack_peek(val=val)
        if nan:
            if self.debug:
                print(f"    value = NaN")
                print(f"     -> {NAN_STRING}")
                print(f"    push value to:{dot_count}")
            self._stack_push([(None, )], dot_count)
        else:
            if self.debug:
                print(f"    value = {numerator}/{denominator}")
                print(f"     -> {numerator // denominator}")
                print(f"    push value to:{dot_count}")
            self._stack_push([(numerator, denominator)], dot_count)
        if self.debug:
            print()

    def heup(self, hangul_count, dot_count, *args,
             full_command=None, line=None, char=None):
        """
        `흡`, `흐읍`, `흐으읍`, `흐으으읍`… : 스택의 위쪽에서 글자
        수만큼의 원소들을 역수로 바꾼 후 그 곱을 마침표 개수에 해당하는
        스택에 넣습니다.

        - 예로 스택이 `1 6 (-3/2) (4/7)`순으로 있고 `4/7`가 다음에 뽑힐
          원소인 상태에서 `흐읍...`을 하면 스택은
          `1 (1/6) (-2/3) (7/4)`가 되고, 3번 스택에 `-7/36`을 넣습니다.
        - `0`의 역수는 `NaN`이 됩니다.
        - `흐`와 `읍` 사이에 `읍`을 제외한 한글 음절 문자를 추가적으로
          넣어 글자 수를 늘릴 수 있습니다.
        """
        if self.debug:
            print(f"{line}:{char} {full_command}")
            print(f" -> {Hyeong._HEUP}({hangul_count}, {dot_count})")

        numerator = denominator = 0
        nan = False
        val = []

        for value in self._stack_peek(hangul_count):
            if value is not None:
                if value != (None, ):
                    val.append((value[1], value[0]))
                    if denominator == 0:
                        numerator, denominator = val[-1]
                    else:
                        numerator *= value[1]
                        denominator *= value[0]
                    numerator, denominator = reduce((numerator, denominator))
                else:
                    val.append((None, ))
                    nan = True

        self._stack_peek(val=val)
        if nan:
            if self.debug:
                print(f"    value = NaN")
                print(f"     -> {NAN_STRING}")
                print(f"    push value to:{dot_count}")
            self._stack_push([(None, )], dot_count)
        else:
            if self.debug:
                print(f"    value = {numerator}/{denominator}")
                print(f"     -> {numerator // denominator}")
                print(f"    push value to:{dot_count}")
            self._stack_push([(numerator, denominator)], dot_count)
        if self.debug:
            print()

    def heuk(self, hangul_count, dot_count, *args,
             full_command=None, line=None, char=None):
        """
        `흑`, `흐윽`, `흐으윽`, `흐으으윽`… : 현재 스택에서 값을 하나
        뽑아, 마침표 개수에 해당하는 스택에 글자 수만큼 복제해서 넣고,
        현재 스택에 뽑았던 값을 하나 넣은 뒤, 마침표 개수에 해당하는
        스택으로 이동합니다.

        - 예를 들어 `흐윽....`은 현재 스택 맨 위에 있는 값을 4번 스택에
          두 개 넣고 4번 스택으로 이동합니다.
        """
        if self.debug:
            print(f"{line}:{char} {full_command}")
            print(f" -> {Hyeong._HEUK}({hangul_count}, {dot_count})")

        val = []

        for value in self._stack_pop(1):
            if value is not None:
                for _ in range(hangul_count):
                    val.append(value)
            self._stack_push(val, dot_count)
            self._stack_push([value])
            self.cursor = dot_count
        if self.debug:
            print()

    def question_mark(self, lt, ge, *args,
                      full_command=None, line=None, char=None):
        """
        `?` : 현재 스택에서 값을 하나 뽑아 글자 수와 마침표 개수를 곱한
        값보다 작으면 물음표보다 앞부분 구역을 실행하고, 크거나 같으면
        뒷부분 구역을 실행합니다. 뽑은 값은 버려집니다.

        - 예를 들어, `혀엉...💗?💕`는 `💕`를 실행합니다.
            1. `혀엉...`으로 스택에 `6`을 집어넣습니다.
            2. 스택에서 값을 뽑습니다. 아까 `6`을 넣었으므로 값은
               `6`입니다.
            3. `혀엉...`에서 글자 수와 마침표 개수를 곱하면 `6`이
               됩니다. 따라서 오른쪽 부분인 `💕`를 실행합니다.
        - 구역 내 물음표가 여러 개일 경우, 맨 왼쪽의 물음표부터
          계산됩니다. `a?b?c`는 `a`, `?`, `b?c`로 나뉩니다.
        - 물음표는 구역 안에서 가장 먼저 계산됩니다. `a!b?c!d`는 `a!b`와
          `c!d`를 `?`로 연결시킨 것으로 해석됩니다.
        """
        pass

    def exclamation_mark(self, eq, ne, *args,
                         full_command=None, line=None, char=None):
        """
        `!` : 현재 스택에서 값을 하나 뽑아 글자 수와 마침표 개수를 곱한
        값과 같으면 느낌표보다 앞부분 구역을 실행하고, 그렇지 않으면
        뒷부분 구역을 실행합니다. 뽑은 값은 버려집니다.

        - 예를 들어, `혀엉...💗?💕`는 `💗`를 실행합니다.
            1. `혀엉...`으로 스택에 `6`을 집어넣습니다.
            2. 스택에서 값을 뽑습니다. 아까 `6`을 넣었으므로 값은
               `6`입니다.
            3. `혀엉...`에서 글자 수와 마침표 개수를 곱하면 `6`이
               됩니다. 따라서 왼쪽 부분인 `💗`를 실행합니다.
        - 구역 내 느낌표가 여러 개일 경우, 맨 왼쪽의 느낌표부터
          계산됩니다. `a!b!c`는 `a`, `!`, `b!c`로 나뉩니다.
        - 느낌표는 구역 안에서 물음표 다음으로 먼저 계산됩니다.
        """
        pass

    def heart(self, quotient, base, *args,
              full_command=None, line=None, char=None):
        pass

    def empty_heart(self, *args, full_command=None, line=None, char=None):
        pass

    _MAP = {
        hyeong: [_HYEONG],
        hang: [_HANG],
        has: [_HAS],
        heus: [_HEUS],
        heup: [_HEUP],
        heuk: [_HEUK],
        heart: [*HEARTS],
        empty_heart: [EMPTY_HEART],
        question_mark: [QUESTION_MARK],
        exclamation_mark: [EXCLAMATION_MARK],
    }

    def __init__(self, code="", debug=False):
        self.code = code
        self.debug = debug

        from sys import stdin, stdout, stderr
        self.stacks = {
            -1: [],
            #: (file, read_fn, write_fn, count_fn),
            0: (stdin, self._in_read, self._in_write, ),
            1: (stdout, (exit, [0], {}), self._out_write),
            2: (stderr, (exit, [1], {}), self._out_write),
            3: [],
        }
        self.cursor = 3

        self.registry = {}

    def __call__(self, code=None, *args):
        if code is not None:
            self.code = code

    def _tokenise(self):
        result = []

        state = ""
        code = self.code + " \n"
        codecount = len(code) - 1
        line = 1
        char = 0
        index = -1
        command = None
        info = ()
        charcount = 0
        dotcount = 0
        from io import StringIO
        area = StringIO()

        flush = False
        clear = False

        while codecount > index:
            index += 1
            char += 1

            # 개행 처리
            crlf = code.startswith("\r\n")
            if crlf or code[index] == "\n":
                line += 1
                char = 1

            # 대기 상태
            if not state:

                if charcount > 0:

                    # 구역
                    if area.tell() % 2 == 0:
                        if charcount:
                            # clear = True
                            pass
                        if code[index] in HEARTS:
                            area.write(code[index])
                    elif area.tell() % 2 == 1:
                        if code[index] == QUESTION_MARK or \
                           code[index] == EXCLAMATION_MARK:
                            area.write(code[index])

                    # "."
                    if code[index] in ELLIPSES:
                        dotcount += 3
                        continue
                    elif code[index] == DOT:
                        dotcount += 1
                        continue

                if flush:
                    if command:
                        if area.tell():
                            result.append((command, 0, 0,
                                           area.getvalue(), info))
                            command = None
                            info = ()
                            area.seek(0)
                            area.truncate()
                            charcount = dotcount = 0
                            flush = False
                        elif charcount:
                            full = code[info[0]:info[0] + charcount + dotcount]
                            result.append((command, charcount, dotcount,
                                           full, info))
                            command = None
                            info = ()
                            charcount = dotcount = 0
                            flush = False
                if flush or clear:
                    if charcount:
                        info = ()
                        charcount = dotcount = 0
                        flush = clear = False
                    elif area.tell():
                        info = ()
                        area.seek(0)
                        area.truncate()
                        flush = clear = False
                # "형"
                if code[index] == Hyeong._HYEONG:
                    command = Hyeong.hyeong
                    charcount = 1
                # "항"
                elif code[index] == Hyeong._HANG:
                    command = Hyeong.hang
                    charcount = 1
                # "핫"
                elif code[index] == Hyeong._HAS:
                    command = Hyeong.has
                    charcount = 1
                # "흣"
                elif code[index] == Hyeong._HEUS:
                    command = Hyeong.heus
                    charcount = 1
                # "흡"
                elif code[index] == Hyeong._HEUP:
                    command = Hyeong.heup
                    charcount = 1
                # "흑"
                elif code[index] == Hyeong._HEUK:
                    command = Hyeong.heuk
                    charcount = 1

                # "하.."
                elif code[index] == Hyeong._HA:
                    charcount = 1
                    state = Hyeong._HA
                # "혀.."
                elif code[index] == Hyeong._HYEO:
                    charcount = 1
                    state = Hyeong._HYEO
                # "흐.."
                elif code[index] == Hyeong._HEU:
                    charcount = 1
                    state = Hyeong._HEU

                else:
                    flush = True

            # "하.."
            elif state == Hyeong._HA:
                if code[index] >= HANGUL_FIRST and code[index] <= HANGUL_LAST:
                    charcount += 1
                    # "..앗"
                    if code[index] == Hyeong._AS:
                        command = Hyeong.has
                        state = ""
                    # "..앙"
                    if code[index] == Hyeong._ANG:
                        command = Hyeong.hang
                        state = ""
            # "혀.."
            elif state == Hyeong._HYEO:
                if code[index] >= HANGUL_FIRST and code[index] <= HANGUL_LAST:
                    charcount += 1
                    # "..엉"
                    if code[index] == Hyeong._EONG:
                        command = Hyeong.hyeong
                        state = ""
            # "흐.."
            elif state == Hyeong._HEU:
                if code[index] >= HANGUL_FIRST and code[index] <= HANGUL_LAST:
                    charcount += 1
                    # "..윽"
                    if code[index] == Hyeong._EUK:
                        command = Hyeong.heuk
                        state = ""
                    # "..읍"
                    elif code[index] == Hyeong._EUP:
                        command = Hyeong.heup
                        state = ""
                    # "..읏"
                    elif code[index] == Hyeong._EUS:
                        command = Hyeong.heus
                        state = ""

            if (command or state) and not info:
                info = (index, line, char)

            # crlf 보정
            if crlf:
                index += 1

        self._flat_token_arr = result
        return result

    # 구문 트리 작성을 위한 명령 우선 순위
    _PRIORITIES = [
        # 1st: 물음표
        [QUESTION_MARK],
        # 2nd: 느낌표
        [EXCLAMATION_MARK],
        # 3rd: 하트
        [EMPTY_HEART, *HEARTS],
        # 4th: 표준 명령
        [_HANG, _HAS, _HYEONG, _HEUK, _HEUP, _HEUS],
    ]

    def _build(self, flat_token_arr=None):
        head = tail = None
        stack = []
        priorities = {}
        index = 0
        for priority in Hyeong._PRIORITIES:
            for group in priority:
                if isinstance(group, str):
                    # priorities[group] = -index
                    for k, v in Hyeong._MAP.items():
                        if group in v:
                            priorities[k] = -index
                            break
                elif isinstance(group, list):
                    for item in group:
                        # priorities[group] = -index
                        for k, v in Hyeong._MAP.items():
                            if item in v:
                                priorities[k] = -index
                                break
            index += 1
        if flat_token_arr is None:
            flat_token_arr = self._flat_token_arr
        for token in flat_token_arr:
            if stack:
                if priorities[stack[-1][0]] > priorities[token[0]]:
                    new = {
                        "token": stack.pop(0),
                        "next_node": None,
                    }
                    if tail:
                        tail["next_node"] = new
                        tail = new
                    else:
                        tail = head = new
                else:
                    stack.append(token)
            else:
                stack.append(token)
        while stack:
            new = {
                "token": stack.pop(0),
                "next_node": None,
            }
            if tail:
                tail["next_node"] = new
                tail = new
            else:
                tail = head = new
        return head

    def _step(self, token, next_node=None, **kwargs):
        token[0](self, token[1], token[2],
                 full_command=token[3], line=token[4][1], char=token[4][2])
        return next_node

    def _run(self, node):
        while node:
            node = self._step(**node)

    def _stack_count(self, cur=None):
        if cur is None:
            cur = self.cursor
        if isinstance(self.stacks[cur], tuple):
            info = self.stacks[cur]
            if isinstance(info[3], tuple):
                info[3][0](*info[3][1], **info[3][2])
            else:
                return info[3](info[0], self.stacks[-1], 0, [])
        else:
            return len(self.stacks[cur])
        return 0

    def _stack_peek(self, cnt=0, val=None, cur=None):
        if cur is None:
            cur = self.cursor
        if val is None:
            # get
            if isinstance(self.stacks[cur], tuple):
                info = self.stacks[cur]
                if isinstance(info[1], tuple):
                    info[1][0](*info[1][1], **info[1][2])
                else:
                    return info[1](info[0], self.stacks[-1], len(val), val)
            else:
                val = []
                for i in range(cnt):
                    if len(self.stacks[cur]):
                        val.append(self.stacks[cur][-i - 1])
                    else:
                        val.append(None)
                return val
        else:
            # set
            if isinstance(self.stacks[cur], tuple):
                info = self.stacks[cur]
                if isinstance(info[2], tuple):
                    info[2][0](*info[2][1], **info[2][2])
                else:
                    return info[2](info[0], self.stacks[-1], len(val), val)
            else:
                cnt = 0
                for value in val:
                    self.stacks[cur][-cnt - 1] = value
                    cnt += 1

    def _stack_push(self, val=None, cur=None):
        if cur is None:
            cur = self.cursor
        if isinstance(self.stacks[cur], tuple):
            info = self.stacks[cur]
            if isinstance(info[2], tuple):
                info[2][0](*info[2][1], **info[2][2])
            else:
                return info[2](info[0], self.stacks[-1], len(val), val)
        cnt = 0
        for value in val:
            self.stacks[cur].append(value)
            cnt += 1
        return cnt

    def _stack_pop(self, cnt=0, cur=None):
        if cur is None:
            cur = self.cursor
        if isinstance(self.stacks[cur], tuple):
            info = self.stacks[cur]
            if isinstance(info[1], tuple):
                info[1][0](*info[1][1], **info[1][2])
            else:
                return info[1](info[0], self.stacks[-1], len(val), val)
        val = []
        for _ in range(cnt):
            if len(self.stacks[cur]):
                val.append(self.stacks[cur].pop())
            else:
                val.append(None)
        return val

    @staticmethod
    def _in_read(f, ex, cnt, val):
        if ex:
            return ex.pop()

    @staticmethod
    def _in_write(f, ex, cnt, val):
        ex.extend(val)
        return len(val)

    @staticmethod
    def _in_count(f, ex, cnt, val):
        if ex:
            return len(ex)

    @staticmethod
    def _out_write(f, ex, cnt, val):
        for _ in range(len(val)):
            value = val.pop()
            if value is (None, ):
                f.write(NAN_STRING)
            elif value[0] // value[1] < 0:
                f.write(str(abs(value[0] // value[1])))
            else:
                f.write(chr(value[0] // value[1]))


def gcd(a, b):
    """
    유클리드 호제법을 이용하여 두 수의 최대공약수를 구합니다.
    """
    while b != 0:
        a, b = b, a % b
    return abs(a)


def reduce(a, b=None):
    """
    주어진 분수를 계산하기 좋은 형태로 변환합니다. 분수는 `(분자, 분모)`
    꼴로 표현됩니다. 하나만 받았을 경우, 약분된 분수를 반환합니다.
    두 개를 받았을 경우, 통분된 분수의 list를 반환합니다.
    """
    if b is None:
        # 약분
        v = gcd(a[0], a[1])
        return a[0] // v, a[1] // v
    else:
        # 통분
        if a[1] != b[1]:
            x = a[0] * b[1]
            y = b[0] * a[1]
            z = a[1] * b[1]
            return [(x, z), (y, z)]
        return [a, b]


def cmp(a, b):
    """
    두 분수를 비교합니다. 분수는 `(분자, 분모)` 꼴로 표현됩니다.
    `a`가 클 경우 양수, 같을 경우 0, `b`가 클 경우 음수를 반환합니다.
    """
    a, b = reduce(a, b)
    return (a[0] > b[0]) - (a[0] < b[0])


# testing
a = Hyeong()#debug=True)
a.code = (
#while False:
    "혀어어어어어어어엉........ 핫. "                    # H  [x]  2
    "혀엉..... 흑... 하앗... 흐윽... 형. 하앙. "         # e  [x]  6
    "혀엉.... 하앙... 흐윽... 항. "                      # l  [x]  4
    "항. "                                               # l  [x]  1
    "형... 하앙. "                                       # o  [x]  2
    "흐으윽... 형... 흡... 혀엉.. 하아아앗. "            # ,  [ ]  5
    "혀엉.. 흡... 흐읍... 형.. 하앗. "                   #    [ ]  5
    "하아앙... 형... 하앙... 흐윽... 혀어어엉.. 하앙. "  # w  [x]  6
    "항. "                                               # o  [x]  1
    "형... 하앙. "                                       # r  [x]  2
    "혀엉.... 하앙. "                                    # l  [x]  2
    "흑... 항. "                                         # d  [ ]  2
    "형... 흡 하앗. "                                    # !  [ ]  3
    "혀엉..... 흑. "                                     # \n [x]  2
    "흣 "                                                #         1 => 44
)

#a.code = "형... 혀엉... 흐읍... "
#a.code = "형.. 혀어엉. 하앗... "
#a.code = "혀엉. 흑... "
#a.code = "형.. 흣... "

from pprint import pprint
b = a._tokenise()
pprint(b, width=100)

#assert len(b) == 44

c = a._build(b)
d = a._run(c)
print()

#pprint(a.stacks[3])


def hyung():
    a = Hyeong()
    a.code = "혀어엉...."
    b = a._tokenise()
    c = a._build(b)
    d = a._run(c)
    assert a.stacks[3][0] == 12


def heup():
    a = Hyeong()
    a.stacks[3].extend([(1, 1), (6, 1), (-3, 2), (4, 7)])
    print("before: ", end="")
    pprint(a.stacks[3])
    a.code = "흐으읍..."
    print(f"code:   {a.code}")
    b = a._tokenise()
    c = a._build(b)
    d = a._run(c)
    print("after:  ", end="")
    pprint(a.stacks[3])
    z = [(1, 1), (1, 6), (-2, 3), (7, 4), (-7, 36)]
    print(f"answer: ", end="")
    pprint(z)


#heup()


# KNOWN ISSUE
# - 코드 끝이 " \n"이 아니면 마지막 명령이 입력되지 않음.
#   (토큰화 시 강제 삽입하는 것으로 우회 중. 로직 수정 필요.)
# - 하트와 느낌표 물음표가 아직 구현되지 않음.
