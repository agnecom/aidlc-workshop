# Unit 3 (주문 및 실시간 통신) - Code Generation Plan

## Unit Context
- Stories: US-03, US-04, US-05, US-07, US-08, US-ERR-02, US-ERR-03, US-ERR-05
- Dependencies: Unit 1 (auth, models), Unit 2 (menu)
- Entities: Order, OrderItem (already defined in Unit 1)

## Steps

- [x] Step 1: Backend — Schemas (order.py, sse.py), OrderRepository, OrderService, SSEManager
- [x] Step 2: Backend — Order Router, SSE Router, main.py 라우터 등록
- [x] Step 3: Backend — Tests (test_order_router.py)
- [x] Step 4: Customer Frontend — CartStore (Pinia), cart service, order service, SSE service
- [x] Step 5: Customer Frontend — CartView, OrderView, OrderHistoryView, router 업데이트
- [x] Step 6: Admin Frontend — order service, SSE service, DashboardView 확장, router 업데이트
- [x] Step 7: Admin Frontend — Tests (DashboardView.test.js)
- [x] Step 8: Plan checkboxes 및 state 업데이트
