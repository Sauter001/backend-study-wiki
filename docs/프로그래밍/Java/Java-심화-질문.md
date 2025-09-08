# Java에 대한 심화 질문

1. JVM의 메모리 구조 (Heap, Stack, Metaspace, GC 영역)의 역할을 설명하고, OOM(OutOfMemoryError)이 발생하는 이유를 구체적으로 말하라.

1. Java의 가비지 컬렉터(GC) 알고리즘 종류 (Serial, Parallel, CMS, G1, ZGC, Shenandoah)와 각각의 특징을 비교하라.

1. Checked Exception과 Unchecked Exception의 차이, 그리고 왜 자바는 두 가지로 나누었는지 설명하라.

1. Java 메모리 모델(JMM, Java Memory Model)에서 volatile 키워드가 보장하는 것은 무엇이며, 보장하지 않는 것은 무엇인가?

1. `synchronized`와 `ReentrantLock`의 차이를 설명하고, 어떤 상황에서 각각을 선택해야 하는가?

1. Java에서 불변 객체(Immutable Object)를 만드는 방법과, 왜 스레드 안정성과 관련이 있는지 설명하라.

1. final 키워드가 클래스, 메서드, 변수에 각각 적용될 때의 차이를 설명하라.

1. 동적 바인딩(dynamic binding)과 정적 바인딩(static binding)의 차이를 예제와 함께 설명하라.

1. Java에서 제네릭(Generics)이 컴파일 후 타입 소거(Type Erasure)되는 이유와 그로 인해 발생하는 제약사항을 말하라.

1. 와일드카드 제네릭(? extends T, ? super T)의 차이와 PECS(Producer Extends, Consumer Super) 원칙을 설명하라.

1. Reflection API의 장점과 단점, 그리고 보안/성능 측면의 문제점을 설명하라.

1. 자바 직렬화(Serialization)의 동작 방식과, serialVersionUID가 필요한 이유는 무엇인가?

1. hashCode()와 equals()를 재정의할 때 반드시 지켜야 하는 규약을 설명하라.

1. 자바 스트림(Stream) API와 컬렉션(Collection) API의 차이점, 그리고 병렬 스트림(parallel stream)의 장단점을 설명하라.

1. 람다(Lambda)와 익명 클래스(Anonymous Class)의 차이, 그리고 함수형 인터페이스(Functional Interface)의 역할은 무엇인가?

1. 자바에서 enum이 단순한 상수 집합 이상의 기능을 제공하는 이유와 활용 사례를 설명하라.

1. String, StringBuilder, StringBuffer의 차이와 각각의 스레드 안정성(thread-safety) 여부를 설명하라.

1. 자바의 ClassLoader 동작 방식과, Parent Delegation Model의 장점과 한계는 무엇인가?

1. JIT(Just-In-Time) 컴파일러의 최적화 방식과, 인터프리터 모드와의 차이를 설명하라.

1. Java에서 Optional 클래스의 사용 목적과, 남용했을 때 발생하는 문제점은 무엇인가?