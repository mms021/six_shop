import { createRouter, createWebHistory } from 'vue-router'
import ProductDetailView from '@/views/ProductDetailView.vue'
import CategoryView from '@/views/CategoryView.vue'
import Home from '@/views/Home.vue'
import Cart from '@/views/Cart.vue'
import Favorites from '@/views/Favorites.vue'
import AdminPanel from '@/views/admin/AdminPanel.vue'
import AdminCategories from '@/views/admin/AdminCategoris.vue'
import AdminCreateProduct from '@/views/admin/AdminCreateProduct.vue'
import AdminOrders from '@/views/admin/AdminOrders.vue'
import Concierge from '@/views/info/Concierge.vue'
import Help from '@/views/info/Help.vue'
import AboutUs from '@/views/info/AboutUs.vue'
import PrivacyPolicy from '@/views/info/PrivacyPolicy.vue'
import TermsOfService from '@/views/info/TermsOfService.vue'
import OrderHistory from '@/views/OrderHistory.vue'


const routes  = [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/category/:id',
      name: 'category',
      component: CategoryView,
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart
    },
    {
      path: '/product/:id',
      name: 'Product',
      component: ProductDetailView
    },
    {
      path: '/favorites',
      name: 'Favorites',
      component: Favorites
    },
    {
      path: '/admin-page',
      name: 'Admin',
      component: AdminPanel
    },
    {
      path: '/admin-page/categories',
      name: 'AdminCategories',
      component: AdminCategories,
    },
    {
      path: '/admin-page/create-product',
      name: 'AdminCreateProduct',
      component: AdminCreateProduct
    },
    {
      path: '/admin-page/edit-product/:id',
      name: 'AdminEditProduct',
      component: AdminCreateProduct
    },
    {
      path: '/admin-page/orders',
      name: 'Orders',
      component: AdminOrders
    },
    {
      path: '/concierge',
      name: 'Concierge',
      component: Concierge
    },
    {
      path: '/help',
      name: 'Help',
      component: Help
    },
    {
      path: '/privacy-policy',
      name: 'PrivacyPolicy',
      component: PrivacyPolicy
    },
    {
      path: '/terms-of-service',
      name: 'TermsOfService',
      component: TermsOfService
    },
    {
      path: '/about',
      name: 'AboutUs',
      component: AboutUs
    },
    {
      path: '/orders',
      name: 'orders',
      component: OrderHistory
    },
  ]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
